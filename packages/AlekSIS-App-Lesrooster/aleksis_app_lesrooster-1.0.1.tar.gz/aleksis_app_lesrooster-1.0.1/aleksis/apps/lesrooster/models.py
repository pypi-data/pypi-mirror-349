import logging
from collections.abc import Sequence
from datetime import date, datetime, time, timedelta
from typing import Optional, Union

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q, QuerySet
from django.http import HttpRequest
from django.utils import timezone
from django.utils.formats import date_format, time_format
from django.utils.functional import classproperty
from django.utils.translation import gettext_lazy as _

import recurrence
from calendarweek import CalendarWeek
from calendarweek.django import i18n_day_abbr_choices_lazy, i18n_day_name_choices_lazy
from model_utils import FieldTracker
from recurrence.fields import RecurrenceField

from aleksis.apps.chronos.models import LessonEvent, SupervisionEvent
from aleksis.apps.cursus.models import Course, CourseBundle, Subject
from aleksis.apps.lesrooster.tasks import sync_validity_range
from aleksis.core.mixins import ExtensibleModel, ExtensiblePolymorphicModel, GlobalPermissionModel
from aleksis.core.models import Group, Holiday, Person, Room, SchoolTerm
from aleksis.core.util.celery_progress import ProgressRecorder, render_progress_page

from .managers import (
    LessonManager,
    LessonQuerySet,
    RoomPropertiesMixin,
    SlotManager,
    SlotQuerySet,
    SupervisionManager,
    SupervisionQuerySet,
    TeacherPropertiesMixin,
    ValidityRangeManager,
    ValidityRangeQuerySet,
)


class ValidityRangeStatus(models.TextChoices):
    """Validity range status."""

    DRAFT = "draft", _("Draft")
    PUBLISHED = "published", _("Published")


class ValidityRange(ExtensibleModel):
    """A validity range is a date range in which certain data are valid."""

    objects = ValidityRangeManager.from_queryset(ValidityRangeQuerySet)()

    school_term = models.ForeignKey(
        SchoolTerm,
        on_delete=models.CASCADE,
        verbose_name=_("School term"),
        related_name="lr_validity_ranges",
    )
    name = models.CharField(verbose_name=_("Name"), max_length=255, blank=True)

    date_start = models.DateField(verbose_name=_("Start date"))
    date_end = models.DateField(verbose_name=_("End date"))

    status = models.CharField(
        verbose_name=_("Status"),
        max_length=255,
        choices=ValidityRangeStatus.choices,
        default=ValidityRangeStatus.DRAFT.value,
    )

    status_tracker = FieldTracker(fields=["status", "date_start", "date_end", "school_term"])

    @property
    def published(self):
        return self.status == ValidityRangeStatus.PUBLISHED.value

    @classmethod
    def get_current(cls, day: Optional[date] = None) -> Optional["ValidityRange"]:
        """Get the currently active validity range."""
        if not day:
            day = timezone.now().date()
        try:
            return cls.objects.on_day(day).first()
        except ValidityRange.DoesNotExist:
            return None

    @classproperty
    def current(cls) -> Optional["ValidityRange"]:
        """Get the currently active validity range."""
        return cls.get_current()

    @property
    def is_current(self) -> bool:
        return self.date_start <= (today := timezone.now().date()) and self.date_end >= today

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            # This is a new ValidityRange being saved for the first time
            # Do the initialization
            TimeboundCourseConfig.create_for_validity_range(self)
            TimeGrid.objects.create(validity_range=self)

    def clean(self):
        """Ensure that there is only one validity range at each point of time."""

        if self.status_tracker.changed().get("status", "") == ValidityRangeStatus.PUBLISHED.value:
            raise ValidationError(_("You can't unpublish a validity range."))

        if self.date_end < self.date_start:
            raise ValidationError(_("The start date must be earlier than the end date."))

        if self.school_term and (
            self.date_end > self.school_term.date_end
            or self.date_start < self.school_term.date_start
        ):
            raise ValidationError(_("The validity range must be within the school term."))

        if self.published:
            errors = {}
            if "school_term" in self.status_tracker.changed():
                errors["school_term"] = _(
                    "The school term of a published validity range can't be changed."
                )

            if "date_start" in self.status_tracker.changed():
                if self.status_tracker.changed()["date_start"] < datetime.now().date():
                    errors["date_start"] = _(
                        "You can't change the start date if the validity range is already active."
                    )
                elif self.date_start < datetime.now().date():
                    errors["date_start"] = _("You can't set the start date to a date in the past.")

            if "date_end" in self.status_tracker.changed():
                if self.status_tracker.changed()["date_end"] < datetime.now().date():
                    errors["date_end"] = _(
                        "You can't change the end date "
                        "if the validity range is already in the past."
                    )
                elif self.date_end < datetime.now().date():
                    errors["date_end"] = _(
                        "To avoid data loss, the validity range can "
                        "be only shortened until the current day."
                    )

            if errors:
                raise ValidationError(errors)

            qs = ValidityRange.objects.within_dates(self.date_start, self.date_end).filter(
                status=ValidityRangeStatus.PUBLISHED
            )
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(
                    _(
                        "There is already a published validity range "
                        "for this time or a part of this time."
                    )
                )

    def publish(self, request: HttpRequest | None = None):
        """Publish this validity range and sync all lessons/supervisions.

        :param request: Optional :class:`HttpRequest` to show progress of syncing in frontend
        """
        self.status = ValidityRangeStatus.PUBLISHED.value
        self.full_clean()
        self.save()
        self.sync(request=request)

    def sync(self, request: HttpRequest | None):
        """Sync all lessons and supervisions of this validity range.

        :params request: Optional request to show progress of syncing in frontend
        """
        if not self.published:
            return
        if not request:
            self._sync()
        else:
            result = sync_validity_range.delay(self.pk)
            return render_progress_page(
                request,
                task_result=result,
                title=_("Publish validity range {}".format(self)),
                progress_title=_(
                    "All lessons and supervisions in the validity range {} are being synced …"
                ).format(self),
                success_message=_("The validity range has been published successfully."),
                error_message=_("There was a problem while publishing the validity range."),
            )

    def _sync(self, recorder: ProgressRecorder | None = None):
        objs_to_update = list(
            LessonBundle.objects.filter(slot_start__time_grid__validity_range=self)
        ) + list(Supervision.objects.filter(break_slot__time_grid__validity_range=self))

        iterate = recorder.iterate(objs_to_update) if recorder else objs_to_update

        for obj in iterate:
            logging.info(f"Syncing object {obj} ({type(obj)}, {obj.pk})")
            obj.sync()

    def __str__(self) -> str:
        return self.name or f"{date_format(self.date_start)}–{date_format(self.date_end)}"

    class Meta:
        verbose_name = _("Validity range")
        verbose_name_plural = _("Validity ranges")
        constraints = [
            models.UniqueConstraint(
                fields=["school_term", "date_start", "date_end"],
                condition=Q(status=ValidityRangeStatus.PUBLISHED),
                name="lr_unique_dates_per_term",
            ),
            models.CheckConstraint(
                check=Q(date_start__lte=F("date_end")), name="date_start_lte_date_end"
            ),
        ]
        indexes = [
            models.Index(fields=["date_start", "date_end"], name="lr_validity_date_start_end")
        ]


class TimeGrid(ExtensibleModel):
    validity_range = models.ForeignKey(
        ValidityRange,
        on_delete=models.CASCADE,
        related_name="time_grids",
        verbose_name=_("Linked validity range"),
    )

    group = models.ForeignKey(
        Group,
        verbose_name=_("Group"),
        on_delete=models.SET_NULL,
        related_name="time_grids",
        blank=True,
        null=True,
    )

    @property
    def times_dict(self) -> dict[int, tuple[datetime, datetime]]:
        slots = {}
        for slot in self.slots.all():
            slots[slot.period] = (slot.time_start, slot.time_end)
        return slots

    @property
    def period_min(self) -> int:
        return self.slots.get_period_min()

    @property
    def period_max(self) -> int:
        return self.slots.get_period_max()

    @property
    def time_min(self) -> time | None:
        return self.slots.get_time_min()

    @property
    def time_max(self) -> time | None:
        return self.slots.get_time_max()

    @property
    def weekday_min(self) -> int:
        return self.slots.get_weekday_min()

    @property
    def weekday_max(self) -> int:
        return self.slots.get_weekday_max()

    def __str__(self):
        if self.group:
            return f"{self.validity_range}: {self.group}"
        return str(self.validity_range)

    class Meta:
        verbose_name = _("Time Grid")
        verbose_name_plural = _("Time Grids")
        constraints = [
            models.UniqueConstraint(
                fields=["validity_range", "group"], name="lr_unique_validity_range_group_time_grid"
            ),
            models.UniqueConstraint(
                fields=["validity_range"], condition=Q(group=None), name="lr_one_default_time_grid"
            ),
        ]


class Slot(ExtensiblePolymorphicModel):
    """A slot is a time period in which a lesson can take place."""

    objects = SlotManager.from_queryset(SlotQuerySet)()

    WEEKDAY_CHOICES = i18n_day_name_choices_lazy()
    WEEKDAY_CHOICES_SHORT = i18n_day_abbr_choices_lazy()

    time_grid = models.ForeignKey(
        TimeGrid,
        on_delete=models.CASCADE,
        related_name="slots",
        verbose_name=_("Time Grid"),
    )

    name = models.CharField(verbose_name=_("Name"), max_length=255, blank=True)

    weekday = models.PositiveSmallIntegerField(
        verbose_name=_("Week day"), choices=i18n_day_name_choices_lazy()
    )
    period = models.PositiveSmallIntegerField(
        verbose_name=_("Number of period"), blank=True, null=True
    )

    time_start = models.TimeField(verbose_name=_("Start time"))
    time_end = models.TimeField(verbose_name=_("End time"))

    def __str__(self) -> str:
        if self.name:
            suffix = self.name
        elif self.period:
            suffix = f"{self.period}."
        else:
            suffix = f"{time_format(self.time_start)}–{time_format(self.time_end)}"
        return f"{self.weekday}, {suffix}"

    def get_date(self, week: CalendarWeek) -> date:
        """Get date of lesson in a specific week."""
        return week[self.weekday]

    def get_datetime_start(self, date_ref: Union[CalendarWeek, date]) -> datetime:
        """Get datetime of lesson start in a specific week or on a specific day."""
        if isinstance(date_ref, date):
            date_ref = CalendarWeek.from_date(date_ref)
        day = self.get_date(date_ref)
        return timezone.make_aware(datetime.combine(day, self.time_start))

    def get_first_datetime(self) -> datetime:
        start = self.get_datetime_start(self.time_grid.validity_range.date_start)
        if start.date() < self.time_grid.validity_range.date_start:
            start = self.get_datetime_start(
                self.time_grid.validity_range.date_start + timedelta(days=7)
            )
        return start

    def get_datetime_end(self, date_ref: Union[CalendarWeek, int, date]) -> datetime:
        """Get datetime of lesson end in a specific week or on a specific day."""
        if isinstance(date_ref, date):
            date_ref = CalendarWeek.from_date(date_ref)
        day = self.get_date(date_ref)
        return timezone.make_aware(datetime.combine(day, self.time_end))

    def get_last_datetime(self) -> datetime:
        end = self.get_datetime_end(self.time_grid.validity_range.date_end)
        if end.date() > self.time_grid.validity_range.date_end:
            end = self.get_datetime_end(self.time_grid.validity_range.date_end - timedelta(days=7))
        return end

    def build_recurrence(
        self, *args, slot_end: Optional["Slot"] = None, **kwargs
    ) -> recurrence.Recurrence:
        """Build a recurrence for this slot respecting the validity range borders."""
        if not slot_end:
            slot_end = self
        pattern = recurrence.Recurrence(
            dtstart=timezone.make_aware(
                datetime.combine(self.time_grid.validity_range.date_start, self.time_start)
            ),
            rrules=[
                recurrence.Rule(
                    *args,
                    **kwargs,
                    until=timezone.make_aware(
                        datetime.combine(self.time_grid.validity_range.date_end, slot_end.time_end)
                    ),
                )
            ],
        )
        return pattern

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["weekday", "period", "time_grid"], name="lr_unique_period_per_range"
            ),
            models.CheckConstraint(
                check=Q(time_start__lte=F("time_end")), name="time_start_lte_time_end"
            ),
        ]
        ordering = ["weekday", "period"]
        indexes = [models.Index(fields=["time_start", "time_end"])]
        verbose_name = _("Slot")
        verbose_name_plural = _("Slots")


class LessonBundle(ExtensibleModel):
    """A lesson bundle represents several lessons with the same slot and recurrence."""

    course_bundle = models.ForeignKey(
        CourseBundle,
        on_delete=models.CASCADE,
        related_name="lesson_bundle",
        verbose_name=_("Course Bundle"),
        null=True,
        blank=True,
    )

    lessons = models.ManyToManyField(
        "Lesson", related_name="bundle", verbose_name=_("Bundled lessons")
    )

    # Allow lesson bundles to go over multiple slots to ensure
    # that they are later tracked as single event
    slot_start = models.ForeignKey(
        Slot,
        on_delete=models.CASCADE,
        verbose_name=_("Start slot"),
        related_name="+",
    )
    slot_end = models.ForeignKey(
        Slot,
        on_delete=models.CASCADE,
        verbose_name=_("End slot"),
        related_name="+",
    )

    # Recurrence rules allow to define a series of lesson bundles
    # Common examples are weekly or every second week
    recurrence = RecurrenceField(
        verbose_name=_("Recurrence"),
        blank=True,
        null=True,
        help_text=_("Leave empty for a single lesson."),
    )

    def clean(self):
        """Ensure that the slots are in the same validity range."""
        if self.slot_start.time_grid != self.slot_end.time_grid:
            raise ValidationError(_("The slots must be in the same time grid."))

    def build_recurrence(self, *args, **kwargs) -> "recurrence.Recurrence":
        """Build a recurrence for this lesson respecting the validity range borders."""
        return self.slot_start.build_recurrence(*args, slot_end=self.slot_end, **kwargs)

    @property
    def real_recurrence(self) -> "recurrence.Recurrence":
        """Get the real recurrence adjusted to the validity range and including holidays."""
        if not self.recurrence:
            return
        rrules = self.recurrence.rrules
        for rrule in rrules:
            rrule.until = self.slot_end.get_last_datetime()
        pattern = recurrence.Recurrence(
            dtstart=self.slot_start.get_first_datetime(),
            rrules=rrules,
        )
        pattern.exdates = Holiday.get_ex_dates(
            self.slot_start.get_first_datetime(), self.slot_end.get_last_datetime(), pattern
        )
        return pattern

    def sync(self) -> Sequence[LessonEvent]:
        """Sync the lesson with its lesson event."""
        week_start = CalendarWeek.from_date(self.slot_start.time_grid.validity_range.date_start)
        datetime_start = self.slot_start.get_datetime_start(week_start)
        datetime_end = self.slot_end.get_datetime_end(week_start)

        lesson_events = []
        for lesson in self.lessons.all():
            lesson_event = LessonEvent() if not lesson.lesson_event else lesson.lesson_event

            lesson_event.slot_number_start = self.slot_start.period
            lesson_event.slot_number_end = self.slot_end.period

            lesson_event.course = lesson.course
            lesson_event.subject = lesson.subject
            lesson_event.datetime_start = datetime_start
            lesson_event.datetime_end = datetime_end

            lesson_event.recurrences = self.real_recurrence

            lesson_event.save()

            if lesson.course:
                lesson_event.groups.set(lesson.course.groups.all())
            else:
                lesson_event.groups.clear()
            lesson_event.teachers.set(lesson.teachers.all())
            lesson_event.rooms.set(lesson.rooms.all())

            if lesson.lesson_event != lesson_event:
                lesson.lesson_event = lesson_event
                lesson.save()

            lesson_events.append(lesson_event)

        return lesson_events

    @classmethod
    def create_from_course_bundle(
        cls,
        course_bundle: CourseBundle,
        validity_range: ValidityRange,
        slot_start: Slot,
        slot_end: Slot,
        recurrence: str,
    ) -> "LessonBundle":
        """Create a lesson bundle from a course bundle."""
        lesson_bundle = cls.objects.create(
            course_bundle=course_bundle,
            slot_start=slot_start,
            slot_end=slot_end,
            recurrence=recurrence,
        )

        lesson_bundle.lessons.set(
            [
                Lesson.create_from_course(course, validity_range)
                for course in course_bundle.courses.all()
            ]
        )

        return lesson_bundle

    class Meta:
        ordering = [
            "slot_start__time_grid__validity_range__date_start",
            "slot_start__weekday",
            "slot_start__time_start",
        ]
        verbose_name = _("Lesson Bundle")
        verbose_name_plural = _("Lesson Bundles")

    def __str__(self):
        course_bundle_name = self.course_bundle.name if self.course_bundle else "–"
        return f"{str(self.slot_start.time_grid.validity_range)}: {course_bundle_name}"


class Lesson(TeacherPropertiesMixin, RoomPropertiesMixin, ExtensibleModel):
    """A lesson represents a single teaching event."""

    objects = LessonManager.from_queryset(LessonQuerySet)()

    lesson_event = models.OneToOneField(
        LessonEvent,
        on_delete=models.SET_NULL,
        related_name="lesson",
        verbose_name=_("Linked lesson event"),
        blank=True,
        null=True,
    )

    # A Course is the base of each lesson, it is its planing base

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name=_("Course"), null=True, blank=True
    )

    # None of the following attributes is required
    # as practice has shown that all possible combinations can occur
    rooms = models.ManyToManyField(
        Room,
        verbose_name=_("Rooms"),
        related_name="lr_lessons",
        blank=True,
    )
    teachers = models.ManyToManyField(
        Person,
        verbose_name=_("Teachers"),
        related_name="lr_lessons_as_teacher",
        blank=True,
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name=_("Subject"),
        related_name="lr_lessons",
        blank=True,
        null=True,
    )

    def get_teachers(self) -> QuerySet[Person]:
        return self.teachers.all()

    def get_rooms(self) -> QuerySet[Room]:
        return self.rooms.all()

    def get_groups(self) -> QuerySet[Group]:
        return self.course.groups.all()

    @classmethod
    def create_from_course(cls, course: Course, validity_range: ValidityRange) -> "Lesson":
        """Create a lesson from a course backed by a validity range."""
        # Lookup the TCC for the course in the validity_range
        tcc = TimeboundCourseConfig.objects.get(course=course, validity_range=validity_range)
        lesson = cls.objects.create(
            course=course,
            subject=course.subject,
        )
        if course.default_room:
            lesson.rooms.set([course.default_room])
        lesson.teachers.set(tcc.teachers.all())
        return lesson

    class Meta:
        ordering = [
            "subject",
        ]
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")


class BreakSlot(Slot):
    """A break is a time period that can supervised and in which no lessons take place."""

    def __str__(self) -> str:
        return f"{time_format(self.time_start)} - {time_format(self.time_end)}"

    class Meta:
        verbose_name = _("Break")
        verbose_name_plural = _("Breaks")


class Supervision(TeacherPropertiesMixin, RoomPropertiesMixin, ExtensibleModel):
    """A supervision is a time period in which a teacher supervises a room."""

    objects = SupervisionManager.from_queryset(SupervisionQuerySet)()

    supervision_event = models.OneToOneField(
        SupervisionEvent,
        on_delete=models.SET_NULL,
        related_name="supervision",
        verbose_name=_("Linked supervision event"),
        blank=True,
        null=True,
    )

    rooms = models.ManyToManyField(
        Room,
        verbose_name=_("Rooms"),
        related_name="lr_supervisions",
    )
    teachers = models.ManyToManyField(
        Person,
        verbose_name=_("Teachers"),
        related_name="lr_supervisions",
    )
    break_slot = models.ForeignKey(
        BreakSlot,
        on_delete=models.CASCADE,
        verbose_name=_("Break Slot"),
        related_name="lr_supervisions",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name=_("Subject"),
        related_name="lr_supervisions",
        blank=True,
        null=True,
    )

    # Recurrence rules allow to define a series of supervisions
    # Common examples are weekly or every second week
    recurrence = RecurrenceField(
        verbose_name=_("Recurrence"),
        blank=True,
        null=True,
        help_text=_("Leave empty for a single supervision."),
    )

    def get_teachers(self) -> QuerySet[Person]:
        return self.teachers.all()

    def get_rooms(self) -> QuerySet[Room]:
        return self.rooms.all()

    def __str__(self):
        return f"{self.break_slot}, {self.room_names} ({self.teacher_names}))"

    class Meta:
        verbose_name = _("Supervision")
        verbose_name_plural = _("Supervisions")

    def build_recurrence(self, *args, **kwargs) -> "recurrence.Recurrence":
        """Build a recurrence for this supervision respecting the validity range borders."""
        return self.break_slot.build_recurrence(*args, **kwargs)

    @property
    def real_recurrence(self) -> "recurrence.Recurrence":
        """Get the real recurrence adjusted to the validity range and including holidays."""
        if not self.recurrence:
            return
        rrules = self.recurrence.rrules
        for rrule in rrules:
            rrule.until = self.break_slot.get_last_datetime()
        pattern = recurrence.Recurrence(
            dtstart=self.break_slot.get_first_datetime(),
            rrules=rrules,
        )
        pattern.exdates = Holiday.get_ex_dates(
            self.break_slot.get_first_datetime(), self.break_slot.get_last_datetime(), pattern
        )
        return pattern

    def sync(self) -> SupervisionEvent:
        """Sync the supervision with its supervision event."""
        week_start = CalendarWeek.from_date(self.break_slot.time_grid.validity_range.date_start)
        datetime_start = self.break_slot.get_datetime_start(week_start)
        datetime_end = self.break_slot.get_datetime_end(week_start)

        supervision_event = self.supervision_event if self.supervision_event else SupervisionEvent()

        supervision_event.datetime_start = datetime_start
        supervision_event.datetime_end = datetime_end
        supervision_event.subject = self.subject

        supervision_event.recurrences = self.real_recurrence

        supervision_event.save()

        supervision_event.teachers.set(self.teachers.all())
        supervision_event.rooms.set(self.rooms.all())

        if self.supervision_event != supervision_event:
            self.supervision_event = supervision_event
            self.save()

        return supervision_event


class TimeboundCourseConfig(ExtensibleModel):
    """A timebound course config is the specific configuration of a course.

    It consists of a course and a validity range.
    """

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name=_("Course"),
        related_name="lr_timebound_course_configs",
    )
    validity_range = models.ForeignKey(
        ValidityRange,
        on_delete=models.CASCADE,
        verbose_name=_("Linked validity range"),
        related_name="lr_timebound_course_configs",
    )

    lesson_quota = models.PositiveSmallIntegerField(
        verbose_name=_("Lesson quota"),
        help_text=_("Number of slots this course is scheduled to fill per week"),
        blank=True,
        null=True,
    )
    teachers = models.ManyToManyField(
        Person,
        verbose_name=_("Teachers"),
        related_name="lr_timebound_course_configs",
    )

    # This seems a bit slow -> @hansegucker please have a look.
    @classmethod
    def create_for_validity_range(
        cls, validity_range: ValidityRange
    ) -> Sequence["TimeboundCourseConfig"]:
        timebound_course_configs = []
        for course in Course.objects.filter(
            Q(groups__school_term__pk=validity_range.school_term.pk)
            | Q(groups__parent_groups__school_term__pk=validity_range.school_term.pk)
        ).distinct():
            tcc = cls.objects.create(
                managed_by_app_label=TimeboundCourseConfig._meta.app_label,
                course=course,
                validity_range=validity_range,
                lesson_quota=course.lesson_quota,
            )
            tcc.teachers.set(course.teachers.all())
            timebound_course_configs.append(tcc)

        return timebound_course_configs

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course", "validity_range"], name="lr_unique_course_config_per_range"
            ),
        ]
        verbose_name = _("Timebound course config")
        verbose_name_plural = _("Timebound course configs")


class LesroosterGlobalPermissions(GlobalPermissionModel):
    class Meta:
        managed = False
        permissions = (
            ("manage_lesson_raster", _("Can manage lesson raster")),
            ("plan_timetables", _("Can plan timetables")),
        )
