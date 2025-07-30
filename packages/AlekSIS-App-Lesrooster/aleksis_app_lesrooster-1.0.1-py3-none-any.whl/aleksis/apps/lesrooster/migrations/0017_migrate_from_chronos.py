import logging
from datetime import datetime, timedelta

from django.apps import apps as global_apps
from django.core.paginator import Paginator
from django.db import migrations, reset_queries
from django.db.models import Count
from django.utils import timezone

import recurrence
from calendarweek import CalendarWeek
from recurrence import serialize
from tqdm import tqdm

logger = logging.getLogger(__name__)


def _build_recurrence(slot):
    pattern = recurrence.Recurrence(
        dtstart=timezone.make_aware(
            datetime.combine(slot.time_grid.validity_range.date_start, slot.time_start)
        ),
        rrules=[
            recurrence.Rule(
                recurrence.WEEKLY,
                until=timezone.make_aware(
                    datetime.combine(slot.time_grid.validity_range.date_end, slot.time_end)
                ),
            )
        ],
    )
    return pattern


def _real_recurrence(lesson, holidays_map):
    rrules = lesson.recurrence.rrules

    slot_start = lesson.slot_start if hasattr(lesson, "slot_start") else lesson.break_slot
    slot_end = lesson.slot_end if hasattr(lesson, "slot_end") else lesson.break_slot
    week_start = CalendarWeek.from_date(slot_start.time_grid.validity_range.date_start)
    week_end = CalendarWeek.from_date(slot_start.time_grid.validity_range.date_end)

    datetime_start = timezone.make_aware(
        datetime.combine(week_start[slot_start.weekday], slot_start.time_start)
    )
    datetime_end = timezone.make_aware(
        datetime.combine(week_end[slot_end.weekday], slot_start.time_end)
    )

    for rrule in rrules:
        rrule.until = datetime_end
    pattern = recurrence.Recurrence(
        dtstart=datetime_start,
        rrules=rrules,
    )
    delta = datetime_end.date() - datetime_start.date()
    for i in range(delta.days + 1):
        holiday_date = datetime_start.date() + timedelta(days=i)
        if holiday_date in holidays_map:
            ex_datetime = timezone.make_aware(datetime.combine(holiday_date, slot_start.time_start))
            pattern.exdates.append(ex_datetime)
    return pattern


def _sync_supervision(apps, schema_editor, supervision, holidays_map):
    SupervisionEvent = apps.get_model("chronos", "SupervisionEvent")
    ContentType = apps.get_model("contenttypes", "ContentType")

    ct_supervision_event = ContentType.objects.get_for_model(SupervisionEvent)

    week_start = CalendarWeek.from_date(supervision.break_slot.time_grid.validity_range.date_start)
    datetime_start = timezone.make_aware(
        datetime.combine(
            week_start[supervision.break_slot.weekday], supervision.break_slot.time_start
        )
    )
    datetime_end = timezone.make_aware(
        datetime.combine(
            week_start[supervision.break_slot.weekday], supervision.break_slot.time_end
        )
    )

    supervision_event = (
        supervision.supervision_event if supervision.supervision_event else SupervisionEvent()
    )

    supervision_event.datetime_start = datetime_start
    supervision_event.datetime_end = datetime_end
    supervision_event.subject = supervision.subject

    supervision_event.recurrences = _real_recurrence(supervision, holidays_map)
    supervision_event.timezone = supervision_event.datetime_start.tzinfo
    supervision_event.exdatetimes = supervision_event.recurrences.exdates
    supervision_event.rdatetimes = supervision_event.recurrences.rdates
    supervision_event.rrule = serialize(supervision_event.recurrences.rrules[0])
    if supervision_event.rrule.startswith("RRULE:"):
        supervision_event.rrule = supervision_event.rrule[6:]

    supervision_event.polymorphic_ctype_id = ct_supervision_event.id

    supervision_event.save()

    supervision_event.teachers.set(supervision.teachers.all())
    supervision_event.rooms.set(supervision.rooms.all())

    supervision.supervision_event = supervision_event
    supervision.save()


def forwards(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")

    Room = apps.get_model("core", "Room")
    Holiday = apps.get_model("core", "Holiday")
    ct_holiday = ContentType.objects.get_for_model(Holiday)

    LessonEvent = apps.get_model("chronos", "LessonEvent")
    SupervisionEvent = apps.get_model("chronos", "SupervisionEvent")
    ct_lesson_event = ContentType.objects.get_for_model(LessonEvent)
    ct_supervision_event = ContentType.objects.get_for_model(SupervisionEvent)

    ChronosSubject = apps.get_model("chronos", "Subject")
    ChronosValidityRange = apps.get_model("chronos", "ValidityRange")
    ChronosTimePeriod = apps.get_model("chronos", "TimePeriod")
    ChronosBreak = apps.get_model("chronos", "Break")
    ChronosLesson = apps.get_model("chronos", "Lesson")
    ChronosLessonPeriod = apps.get_model("chronos", "LessonPeriod")
    ChronosSupervisionArea = apps.get_model("chronos", "SupervisionArea")
    ChronosSupervision = apps.get_model("chronos", "Supervision")
    ChronosLessonSubstitution = apps.get_model("chronos", "LessonSubstitution")
    ChronosSupervisionSubstitution = apps.get_model("chronos", "SupervisionSubstitution")
    ChronosEvent = apps.get_model("chronos", "Event")
    ChronosExtraLesson = apps.get_model("chronos", "ExtraLesson")
    ChronosHoliday = apps.get_model("chronos", "Holiday")
    ChronosAbsenceReason = apps.get_model("chronos", "AbsenceReason")
    ChronosAbsence = apps.get_model("chronos", "Absence")

    CursusSubject = apps.get_model("cursus", "Subject")
    CursusCourse = apps.get_model("cursus", "Course")

    LesroosterValidityRange = apps.get_model("lesrooster", "ValidityRange")
    LesroosterTimeGrid = apps.get_model("lesrooster", "TimeGrid")
    LesroosterSlot = apps.get_model("lesrooster", "Slot")
    LesroosterBreakSlot = apps.get_model("lesrooster", "BreakSlot")
    LesroosterLesson = apps.get_model("lesrooster", "Lesson")
    LesroosterSupervision = apps.get_model("lesrooster", "Supervision")

    subject_map = {}
    for subject in tqdm(ChronosSubject.objects.iterator(), "Subjects"):
        cursus_subject = CursusSubject.objects.create(
            short_name=subject.short_name,
            name=subject.name,
            colour_fg=subject.colour_fg,
            colour_bg=subject.colour_bg,
            extended_data=subject.extended_data,
        )
        subject_map[subject.id] = cursus_subject

    validity_range_map = {}
    time_grid_map = {}
    for validity_range in tqdm(ChronosValidityRange.objects.iterator(), "Validity Ranges"):
        lesrooster_validity_range = LesroosterValidityRange.objects.create(
            school_term_id=validity_range.school_term_id,
            name=validity_range.name,
            date_start=validity_range.date_start,
            date_end=validity_range.date_end,
            status="published",
            extended_data=validity_range.extended_data,
        )
        time_grid = LesroosterTimeGrid.objects.create(
            validity_range_id=lesrooster_validity_range.id
        )
        validity_range_map[validity_range.id] = lesrooster_validity_range
        time_grid_map[validity_range.id] = time_grid

    slot_map = {}
    for time_period in tqdm(ChronosTimePeriod.objects.iterator(), "Time Periods"):
        time_grid = time_grid_map[time_period.validity_id]
        lesrooster_slot = LesroosterSlot.objects.create(
            time_grid_id=time_grid.id,
            weekday=time_period.weekday,
            period=time_period.period,
            time_start=time_period.time_start,
            time_end=time_period.time_end,
            extended_data=time_period.extended_data,
        )
        slot_map[time_period.id] = lesrooster_slot

    break_slot_map = {}
    for break_ in tqdm(ChronosBreak.objects.iterator(), "Breaks"):
        weekday = (
            break_.after_period.weekday if break_.after_period else break_.before_period.weekday
        )

        time_start = break_.after_period.time_end if break_.after_period else None
        time_end = break_.before_period.time_start if break_.before_period else None
        if not time_start:
            time_start = time_end
        if not time_end:
            time_end = time_start

        time_grid = time_grid_map[break_.validity_id]
        lesrooster_slot = LesroosterBreakSlot.objects.create(
            time_grid_id=time_grid.id,
            weekday=weekday,
            time_start=time_start,
            time_end=time_end,
            extended_data=break_.extended_data,
        )

        break_slot_map[break_.id] = lesrooster_slot

    holiday_map = {}
    holiday_dates = {}
    for holiday in tqdm(ChronosHoliday.objects.iterator(), "Holidays"):
        core_holiday = Holiday.objects.create(
            holiday_name=holiday.title,
            date_start=holiday.date_start,
            date_end=holiday.date_end,
            extended_data=holiday.extended_data,
            polymorphic_ctype_id=ct_holiday.id,
        )
        delta = holiday.date_end - holiday.date_start
        for i in range(delta.days + 1):
            holiday_date = holiday.date_start + timedelta(days=i)
            holiday_dates.setdefault(holiday_date, []).append(core_holiday)
        holiday_map[holiday.id] = core_holiday

    course_map = {}
    lesson_map = {}
    qs = ChronosLesson.objects.prefetch_related("groups", "teachers").order_by("id")
    paginator = Paginator(qs, 1000)
    for page_number in tqdm(
        paginator.page_range,
        "Lessons",
    ):
        page = paginator.page(page_number)
        create_list_course_groups = []
        create_list_course_teachers = []
        create_list_lesson_teachers = []
        create_list_lesson_rooms = []
        create_list_lesson_event_groups = []
        create_list_lesson_event_teachers = []
        create_list_lesson_event_rooms = []
        for lesson in tqdm(page.object_list):
            subject = subject_map[lesson.subject_id]
            possible_courses = CursusCourse.objects.annotate(groups_count=Count("groups")).filter(
                subject_id=subject.id,
                groups__in=lesson.groups.all(),
                groups_count=len(lesson.groups.all()),
            )
            course = None
            if possible_courses:
                course = possible_courses[0]

            if not course:
                name = "{}: {}".format(
                    ", ".join([c.short_name or c.name for c in lesson.groups.all()]),
                    subject.short_name or subject.name,
                )
                course = CursusCourse.objects.create(subject_id=subject.id, name=name)
            create_list_course_groups += [
                CursusCourse.groups.through(group_id=c.id, course_id=course.id)
                for c in lesson.groups.all()
            ]
            create_list_course_teachers += [
                CursusCourse.teachers.through(person_id=c.id, course_id=course.id)
                for c in lesson.teachers.all()
            ]
            course_map[lesson.id] = course

            # FIXME Check that TCC is created (should be done automatically by @permcu's changes)

            for lesson_period in ChronosLessonPeriod.objects.filter(lesson=lesson).all():
                slot = slot_map[lesson_period.period_id]

                lesrooster_lesson = LesroosterLesson.objects.create(
                    course_id=course.id,
                    slot_start_id=slot.id,
                    slot_end_id=slot.id,
                    recurrence=_build_recurrence(slot),
                    subject_id=subject.id,
                    extended_data=lesson_period.extended_data,
                )

                create_list_lesson_teachers += [
                    LesroosterLesson.teachers.through(
                        person_id=c.id, lesson_id=lesrooster_lesson.id
                    )
                    for c in lesson.teachers.all()
                ]
                if lesson_period.room_id:
                    create_list_lesson_rooms.append(
                        LesroosterLesson.rooms.through(
                            room_id=lesson_period.room_id, lesson_id=lesrooster_lesson.id
                        )
                    )

                # Sync to lesson event

                week_start = CalendarWeek.from_date(slot.time_grid.validity_range.date_start)
                datetime_start = timezone.make_aware(
                    datetime.combine(week_start[slot.weekday], slot.time_start)
                )
                datetime_end = timezone.make_aware(
                    datetime.combine(week_start[slot.weekday], slot.time_end)
                )

                lesson_event = LessonEvent()

                lesson_event.slot_number_start = slot.period
                lesson_event.slot_number_end = slot.period

                lesson_event.course = course
                lesson_event.subject = subject
                lesson_event.datetime_start = datetime_start
                lesson_event.datetime_end = datetime_end

                lesson_event.recurrences = _real_recurrence(lesrooster_lesson, holiday_dates)
                lesson_event.timezone = lesson_event.datetime_start.tzinfo
                lesson_event.exdatetimes = lesson_event.recurrences.exdates
                lesson_event.rdatetimes = lesson_event.recurrences.rdates
                lesson_event.rrule = serialize(lesson_event.recurrences.rrules[0])
                if lesson_event.rrule.startswith("RRULE:"):
                    lesson_event.rrule = lesson_event.rrule[6:]

                lesson_event.polymorphic_ctype_id = ct_lesson_event.id

                lesson_event.lesson = lesrooster_lesson
                lesson_event.save()

                create_list_lesson_event_teachers += [
                    LessonEvent.teachers.through(person_id=c.id, lessonevent_id=lesson_event.id)
                    for c in lesson.teachers.all()
                ]
                create_list_lesson_event_groups += [
                    LessonEvent.groups.through(group_id=c.id, lessonevent_id=lesson_event.id)
                    for c in lesson.groups.all()
                ]
                if lesson_period.room_id:
                    create_list_lesson_event_rooms.append(
                        LessonEvent.rooms.through(
                            room_id=lesson_period.room_id, lessonevent_id=lesson_event.id
                        )
                    )

                logger.info(f"Imported {lesson_period.id} as {lesrooster_lesson.id}")
                lesson_map[lesson_period.id] = lesrooster_lesson

        CursusCourse.groups.through.objects.bulk_create(
            create_list_course_groups, ignore_conflicts=True
        )
        CursusCourse.teachers.through.objects.bulk_create(
            create_list_course_teachers, ignore_conflicts=True
        )
        LessonEvent.groups.through.objects.bulk_create(
            create_list_lesson_event_groups, ignore_conflicts=True
        )
        LessonEvent.teachers.through.objects.bulk_create(
            create_list_lesson_event_teachers, ignore_conflicts=True
        )
        LessonEvent.rooms.through.objects.bulk_create(
            create_list_lesson_event_rooms, ignore_conflicts=True
        )

    supervision_room_map = {}
    for supervision_area in tqdm(ChronosSupervisionArea.objects.all(), "Supervision Areas"):
        room = Room.objects.create(
            short_name=f"Area: {supervision_area.short_name}",
            name=f"Area: {supervision_area.name}",
            extended_data=supervision_area.extended_data,
        )
        supervision_room_map[supervision_area.id] = room

    supervision_map = {}
    for supervision in tqdm(ChronosSupervision.objects.iterator(), "Supervisions"):
        break_slot = break_slot_map[supervision.break_item_id]
        room = supervision_room_map[supervision.area_id]
        lesrooster_supervision = LesroosterSupervision.objects.create(
            break_slot=break_slot,
            recurrence=_build_recurrence(break_slot),
            extended_data=supervision.extended_data,
        )
        lesrooster_supervision.rooms.add(room.id)
        lesrooster_supervision.teachers.add(supervision.teacher_id)

        # Sync to supervision event
        _sync_supervision(apps, schema_editor, lesrooster_supervision, holiday_dates)

        supervision_map[supervision.id] = lesrooster_supervision

    substitution_map = {}
    paginator = Paginator(ChronosLessonSubstitution.objects.order_by("id"), 1000)
    for page_number in tqdm(paginator.page_range, "Lesson Substitutions"):
        page = paginator.page(page_number)
        create_list_lesson_event_teachers = []
        create_list_lesson_event_rooms = []
        for lesson_substitution in tqdm(page.object_list):
            lesson = lesson_map[lesson_substitution.lesson_period_id]

            week = CalendarWeek(week=lesson_substitution.week, year=lesson_substitution.year)

            datetime_start = timezone.make_aware(
                datetime.combine(week[lesson.slot_start.weekday], lesson.slot_start.time_start)
            )
            datetime_end = timezone.make_aware(
                datetime.combine(week[lesson.slot_end.weekday], lesson.slot_end.time_end)
            )

            new_substitution = LessonEvent.objects.create(
                amends=lesson.lesson_event,
                datetime_start=datetime_start,
                datetime_end=datetime_end,
                subject=subject_map.get(lesson_substitution.subject_id),
                cancelled=lesson_substitution.cancelled,
                comment=lesson_substitution.comment,
                extended_data=lesson_substitution.extended_data,
                polymorphic_ctype_id=ct_lesson_event.id,
            )

            create_list_lesson_event_teachers += [
                LessonEvent.teachers.through(person_id=c.id, lessonevent_id=new_substitution.id)
                for c in lesson_substitution.teachers.all()
            ]
            if lesson_substitution.room_id:
                create_list_lesson_event_rooms.append(
                    LessonEvent.rooms.through(
                        room_id=lesson_substitution.room_id, lessonevent_id=new_substitution.id
                    )
                )
            substitution_map.setdefault(lesson_substitution.lesson_period_id, {})
            substitution_map[lesson_substitution.lesson_period_id].setdefault(
                lesson_substitution.year, {}
            )
            substitution_map[lesson_substitution.lesson_period_id][lesson_substitution.year][
                lesson_substitution.week
            ] = new_substitution
        LessonEvent.teachers.through.objects.bulk_create(create_list_lesson_event_teachers)
        LessonEvent.rooms.through.objects.bulk_create(create_list_lesson_event_rooms)

    for supervision_substitution in tqdm(
        ChronosSupervisionSubstitution.objects.iterator(), "Supervision Substitutions"
    ):
        supervision = supervision_map[supervision_substitution.supervision_id]

        day = supervision_substitution.date

        datetime_start = timezone.make_aware(
            datetime.combine(day, supervision.break_slot.time_start)
        )
        datetime_end = timezone.make_aware(datetime.combine(day, supervision.break_slot.time_end))

        new_substitution = SupervisionEvent.objects.create(
            amends_id=supervision.supervision_event_id,
            datetime_start=datetime_start,
            datetime_end=datetime_end,
            extended_data=supervision_substitution.extended_data,
            polymorphic_ctype_id=ct_supervision_event.id,
        )

        new_substitution.teachers.add(supervision_substitution.teacher)

    event_map = {}
    for event in tqdm(
        ChronosEvent.objects.prefetch_related("teachers", "groups", "rooms").iterator(
            chunk_size=2000
        ),
        "Events",
    ):
        slot_from = slot_map[event.period_from_id]
        slot_to = slot_map[event.period_to_id]
        datetime_start = timezone.make_aware(
            datetime.combine(event.date_start, slot_from.time_start)
        )
        datetime_end = timezone.make_aware(datetime.combine(event.date_end, slot_to.time_end))
        lesson_event = LessonEvent.objects.create(
            title=event.title,
            slot_number_start=slot_from.period,
            slot_number_end=slot_to.period,
            datetime_start=datetime_start,
            datetime_end=datetime_end,
            extended_data=event.extended_data,
            polymorphic_ctype_id=ct_lesson_event.id,
        )

        lesson_event.teachers.set(event.teachers.all())
        lesson_event.groups.set(event.groups.all())
        lesson_event.rooms.set(event.rooms.all())

        event_map[event.id] = lesson_event

    extra_lesson_map = {}
    for extra_lesson in tqdm(
        ChronosExtraLesson.objects.prefetch_related("teachers", "groups").iterator(chunk_size=2000),
        "Extra Lessons",
    ):
        slot = slot_map[extra_lesson.period_id]
        week = CalendarWeek(week=extra_lesson.week, year=extra_lesson.year)
        datetime_start = timezone.make_aware(datetime.combine(week[slot.weekday], slot.time_start))
        datetime_end = timezone.make_aware(datetime.combine(week[slot.weekday], slot.time_end))
        lesson_event = LessonEvent.objects.create(
            slot_number_start=slot.period,
            slot_number_end=slot.period,
            datetime_start=datetime_start,
            datetime_end=datetime_end,
            subject=subject_map.get(extra_lesson.subject_id, None),
            comment=extra_lesson.comment,
            extended_data=extra_lesson.extended_data,
            polymorphic_ctype_id=ct_lesson_event.id,
        )

        lesson_event.teachers.set(extra_lesson.teachers.all())
        lesson_event.groups.set(extra_lesson.groups.all())
        if extra_lesson.room_id:
            lesson_event.rooms.add(extra_lesson.room_id)

        extra_lesson_map[extra_lesson.id] = lesson_event

    if global_apps.is_installed("aleksis.apps.kolego"):
        KolegoAbsenceReason = apps.get_model("kolego", "AbsenceReason")
        KolegoAbsence = apps.get_model("kolego", "Absence")
        ct_kolego_absence = ContentType.objects.get_for_model(KolegoAbsence)

        absence_reason_map = {}
        for absence_reason in tqdm(ChronosAbsenceReason.objects.iterator(), "Absence Reasons"):
            kolego_absence_reason = KolegoAbsenceReason.objects.create(
                name=absence_reason.name,
                short_name=absence_reason.short_name,
                extended_data=absence_reason.extended_data,
            )
            absence_reason_map[absence_reason.id] = kolego_absence_reason

        default_absence_reason = KolegoAbsenceReason.objects.get_or_create(
            short_name="?", defaults={"name": "?"}
        )

        for absence in tqdm(ChronosAbsence.objects.filter(teacher__isnull=False), "Absences"):
            slot_from = slot_map[absence.period_from_id]
            slot_to = slot_map[absence.period_to_id]
            datetime_start = timezone.make_aware(
                datetime.combine(absence.date_start, slot_from.time_start)
            )
            datetime_end = timezone.make_aware(datetime.combine(absence.date_end, slot_to.time_end))

            absence_reason = absence_reason_map.get(absence.reason_id) or default_absence_reason

            kolego_absence = KolegoAbsence.objects.create(
                datetime_start=datetime_start,
                datetime_end=datetime_end,
                reason_id=absence_reason.id,
                comment=absence.comment,
                person_id=absence.teacher_id,
                extended_data=absence.extended_data,
                polymorphic_ctype_id=ct_kolego_absence.id,
            )

    if global_apps.is_installed("aleksis.apps.alsijil"):
        if not global_apps.is_installed("aleksis.apps.kolego"):
            raise RuntimeError(
                "To migrate from AlekSIS-App-Alsijil, you need to install AlekSIS-App-Kolego."
            )

        AlsijilExcuseType = apps.get_model("alsijil", "ExcuseType")
        AlsijilLessonDocumentation = apps.get_model("alsijil", "LessonDocumentation")
        AlsijilDocumentation = apps.get_model("alsijil", "Documentation")
        AlsijilPersonalNote = apps.get_model("alsijil", "PersonalNote")
        AlsijilParticipationStatus = apps.get_model("alsijil", "ParticipationStatus")
        AlsijilNewPersonalNote = apps.get_model("alsijil", "NewPersonalNote")
        ct_documentation = ContentType.objects.get_for_model(AlsijilDocumentation)
        ct_participation_status = ContentType.objects.get_for_model(AlsijilParticipationStatus)

        excuse_type_map = {}
        for excuse_type in tqdm(AlsijilExcuseType.objects.iterator(), "Excuse Types"):
            kolego_absence_reason = KolegoAbsenceReason.objects.create(
                name=excuse_type.name,
                short_name=excuse_type.short_name,
                count_as_absent=excuse_type.count_as_absent,
                extended_data=excuse_type.extended_data,
            )
            excuse_type_map[excuse_type.id] = kolego_absence_reason

        documentation_map_lessons = {}
        documentation_map_events = {}
        documentation_map_extra_lessons = {}
        paginator = Paginator(AlsijilLessonDocumentation.objects.order_by("id"), 1000)
        for page_number in tqdm(paginator.page_range, "Lesson Documentations"):
            page = paginator.page(page_number)
            create_list_documentation = []
            create_list_documentation_teachers = []
            for lesson_documentation in tqdm(page.object_list):
                if lesson_documentation.lesson_period_id:
                    lesson = lesson_map[lesson_documentation.lesson_period_id]

                    original_amends = lesson.lesson_event
                    amends = original_amends
                    if (
                        lesson_documentation.lesson_period_id in substitution_map
                        and lesson_documentation.year
                        in substitution_map[lesson_documentation.lesson_period_id]
                        and lesson_documentation.week
                        in substitution_map[lesson_documentation.lesson_period_id][
                            lesson_documentation.year
                        ]
                    ):
                        amends = substitution_map[lesson_documentation.lesson_period_id][
                            lesson_documentation.year
                        ][lesson_documentation.week]
                    week = CalendarWeek(
                        week=lesson_documentation.week, year=lesson_documentation.year
                    )

                    datetime_start = timezone.make_aware(
                        datetime.combine(
                            week[lesson.slot_start.weekday], lesson.slot_start.time_start
                        )
                    )
                    datetime_end = timezone.make_aware(
                        datetime.combine(week[lesson.slot_end.weekday], lesson.slot_end.time_end)
                    )
                elif lesson_documentation.event_id:
                    original_amends = amends = event_map[lesson_documentation.event_id]
                    datetime_start = amends.datetime_start
                    datetime_end = amends.datetime_end
                else:
                    original_amends = amends = extra_lesson_map[
                        lesson_documentation.extra_lesson_id
                    ]
                    datetime_start = amends.datetime_start
                    datetime_end = amends.datetime_end

                new_documentation = AlsijilDocumentation.objects.create(
                    datetime_start=datetime_start,
                    datetime_end=datetime_end,
                    amends_id=amends.id,
                    topic=lesson_documentation.topic,
                    homework=lesson_documentation.homework,
                    group_note=lesson_documentation.group_note,
                    course_id=original_amends.course_id,
                    subject_id=amends.subject_id or original_amends.subject_id,
                    participation_touched_at=datetime_start,
                    polymorphic_ctype_id=ct_documentation.id,
                )
                create_list_documentation.append(new_documentation)
                create_list_documentation_teachers += [
                    AlsijilDocumentation.teachers.through(
                        documentation_id=new_documentation.id, person_id=c.id
                    )
                    for c in list(amends.teachers.all()) + list(original_amends.teachers.all())
                ]

                if lesson_documentation.lesson_period_id:
                    documentation_map_lessons.setdefault(lesson_documentation.lesson_period_id, {})
                    documentation_map_lessons[lesson_documentation.lesson_period_id].setdefault(
                        lesson_documentation.year, {}
                    )
                    documentation_map_lessons[lesson_documentation.lesson_period_id][
                        lesson_documentation.year
                    ][lesson_documentation.week] = new_documentation
                elif lesson_documentation.event_id:
                    documentation_map_events[lesson_documentation.event_id] = new_documentation
                else:
                    documentation_map_extra_lessons[
                        lesson_documentation.extra_lesson_id
                    ] = new_documentation

            AlsijilDocumentation.teachers.through.objects.bulk_create(
                create_list_documentation_teachers, ignore_conflicts=True
            )
            reset_queries()

        absent_absence_reason, __ = KolegoAbsenceReason.objects.update_or_create(
            short_name="a", defaults={"name": "absent", "default": True, "count_as_absent": True}
        )
        excused_absence_reason, __ = KolegoAbsenceReason.objects.update_or_create(
            short_name="e", defaults={"name": "excused", "count_as_absent": True}
        )

        paginator = Paginator(
            AlsijilPersonalNote.objects.prefetch_related(
                "extra_marks", "groups_of_person"
            ).order_by("id"),
            1000,
        )
        key_counter = 0
        for page_number in tqdm(
            paginator.page_range,
            "Personal Notes",
        ):
            page = paginator.page(page_number)
            create_list_groups_of_person = []
            create_list_personal_note = []
            for personal_note in tqdm(page.object_list):
                if personal_note.lesson_period_id:
                    try:
                        documentation = documentation_map_lessons[personal_note.lesson_period_id][
                            personal_note.year
                        ][personal_note.week]
                    except KeyError:
                        lesson = lesson_map[personal_note.lesson_period_id]
                        week = CalendarWeek(week=personal_note.week, year=personal_note.year)

                        datetime_start = timezone.make_aware(
                            datetime.combine(
                                week[lesson.slot_start.weekday], lesson.slot_start.time_start
                            )
                        )
                        datetime_end = timezone.make_aware(
                            datetime.combine(
                                week[lesson.slot_end.weekday], lesson.slot_end.time_end
                            )
                        )

                        documentation = AlsijilDocumentation.objects.create(
                            datetime_start=datetime_start,
                            datetime_end=datetime_end,
                            amends_id=lesson.lesson_event_id,
                            course_id=lesson.course_id,
                            subject_id=lesson.subject_id,
                            participation_touched_at=datetime_start,
                            polymorphic_ctype_id=ct_documentation.id,
                        )
                        documentation.teachers.set(lesson.teachers.all())
                        documentation_map_lessons.setdefault(personal_note.lesson_period_id, {})
                        documentation_map_lessons[personal_note.lesson_period_id].setdefault(
                            personal_note.year, {}
                        )
                        documentation_map_lessons[personal_note.lesson_period_id][
                            personal_note.year
                        ][personal_note.week] = documentation
                        logger.info(
                            f"Created documentation for {personal_note.lesson_period_id} {personal_note.year} {personal_note.week}"
                        )
                        key_counter += 1

                elif personal_note.event_id:
                    documentation = documentation_map_events.get(personal_note.event_id)
                    if not documentation:
                        event = event_map[personal_note.event_id]
                        documentation = AlsijilDocumentation.objects.create(
                            datetime_start=event.datetime_start,
                            datetime_end=event.datetime_end,
                            amends_id=event.id,
                            course_id=event.course_id,
                            subject_id=event.subject_id,
                            participation_touched_at=event.datetime_start,
                            polymorphic_ctype_id=ct_documentation.id,
                        )
                        documentation.teachers.set(event.teachers.all())
                        documentation_map_events[personal_note.event_id] = documentation
                else:
                    documentation = documentation_map_extra_lessons.get(
                        personal_note.extra_lesson_id
                    )
                    if not documentation:
                        extra_lesson = extra_lesson_map[personal_note.extra_lesson_id]
                        documentation = AlsijilDocumentation.objects.create(
                            datetime_start=extra_lesson.datetime_start,
                            datetime_end=extra_lesson.datetime_end,
                            amends_id=extra_lesson.id,
                            course_id=extra_lesson.course_id,
                            subject_id=extra_lesson.subject_id,
                            participation_touched_at=extra_lesson.datetime_start,
                            polymorphic_ctype_id=ct_documentation.id,
                        )
                        documentation.teachers.set(extra_lesson.teachers.all())
                        documentation_map_extra_lessons[
                            personal_note.extra_lesson_id
                        ] = documentation

                absence_reason = None
                if personal_note.absent and personal_note.excuse_type:
                    absence_reason = excuse_type_map[personal_note.excuse_type_id]
                elif personal_note.absent and personal_note.excused:
                    absence_reason = excused_absence_reason
                elif personal_note.absent:
                    absence_reason = absent_absence_reason

                logger.info(
                    f"Create participation status for person {personal_note.person_id} and documentation {documentation.id} out of {personal_note.id}"
                )

                participation_status = AlsijilParticipationStatus.objects.create(
                    person_id=personal_note.person_id,
                    related_documentation_id=documentation.id,
                    datetime_start=documentation.datetime_start,
                    datetime_end=documentation.datetime_end,
                    tardiness=personal_note.tardiness,
                    absence_reason_id=absence_reason.id if absence_reason else None,
                    polymorphic_ctype_id=ct_participation_status.id,
                )

                create_list_groups_of_person += [
                    AlsijilParticipationStatus.groups_of_person.through(
                        participationstatus_id=participation_status.id, group_id=c.id
                    )
                    for c in personal_note.groups_of_person.all()
                ]

                if personal_note.remarks:
                    create_list_personal_note.append(
                        AlsijilNewPersonalNote(
                            person=personal_note.person,
                            note=personal_note.remarks,
                            documentation_id=documentation.id,
                        )
                    )

                for extra_mark in personal_note.extra_marks.all():
                    create_list_personal_note.append(
                        AlsijilNewPersonalNote(
                            person=personal_note.person,
                            extra_mark_id=extra_mark.id,
                            documentation_id=documentation.id,
                        )
                    )

            AlsijilParticipationStatus.groups_of_person.through.objects.bulk_create(
                create_list_groups_of_person, ignore_conflicts=True
            )
            AlsijilNewPersonalNote.objects.bulk_create(
                create_list_personal_note, ignore_conflicts=True
            )
            reset_queries()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0064_rrule_model"),
        ("chronos", "0018_check_new_models"),
        ("cursus", "0003_drop_site"),
        ("lesrooster", "0016_remove_substitutions"),
    ]
    run_before = [
        ("chronos", "0019_remove_old_models"),
    ]

    if global_apps.is_installed("aleksis.apps.kolego"):
        dependencies.append(("kolego", "0004_absencereasontag_absencereason_tags"))
    if global_apps.is_installed("aleksis.apps.alsijil"):
        dependencies.append(("alsijil", "0024_check_new_models"))
        run_before.append(("alsijil", "0025_remove_old_models"))

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
