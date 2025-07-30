from datetime import date, time

import pytest
import recurrence
from calendarweek import CalendarWeek

from aleksis.apps.cursus.models import Course, Subject
from aleksis.apps.lesrooster.models import (
    BreakSlot,
    Lesson,
    LessonBundle,
    Slot,
    Supervision,
    TimeGrid,
    ValidityRange,
    ValidityRangeStatus,
)
from aleksis.core.models import Group, Person, Room, SchoolTerm

pytestmark = pytest.mark.django_db(databases=["default", "default_oot"])


@pytest.fixture
def school_term():
    date_start = date(2024, 1, 1)
    date_end = date(2024, 6, 1)
    school_term = SchoolTerm.objects.get_or_create(
        name="Test", date_start=date_start, date_end=date_end
    )[0]
    return school_term


@pytest.fixture
def validity_range(school_term):
    validity_range = ValidityRange.objects.get_or_create(
        school_term=school_term, date_start=school_term.date_start, date_end=school_term.date_end
    )[0]
    return validity_range


@pytest.fixture
def time_grid(validity_range):
    return TimeGrid.objects.get_or_create(validity_range=validity_range, group=None)[0]


@pytest.fixture
def lesson(time_grid):
    slot_a = Slot.objects.create(
        time_grid=time_grid, weekday=0, period=1, time_start=time(8, 0), time_end=time(9, 0)
    )
    slot_b = Slot.objects.create(
        time_grid=time_grid, weekday=0, period=2, time_start=time(9, 0), time_end=time(10, 0)
    )

    subject = Subject.objects.create(name="Math", short_name="Ma")

    course_teachers = [
        Person.objects.create(first_name=f"course_{i}", last_name=f"{i}") for i in range(2)
    ]
    course_groups = [Group.objects.create(name=f"course_{i}") for i in range(2)]

    course_subject = Subject.objects.create(name="English", short_name="En")
    course = Course.objects.create(name="Testcourse", subject=course_subject)
    course.groups.set(course_groups)
    course.teachers.set(course_teachers)

    teachers = [Person.objects.create(first_name=f"lesson_{i}", last_name=f"{i}") for i in range(2)]
    rooms = [Room.objects.create(name=f"lesson_{i}", short_name=f"lesson_{i}") for i in range(2)]

    lesson = Lesson.objects.create(course=course, subject=subject)
    lesson.teachers.set(teachers)
    lesson.rooms.set(rooms)
    lesson_bundle = LessonBundle.objects.create(slot_start=slot_a, slot_end=slot_b)
    lesson_bundle.lessons.add(lesson)
    lesson_bundle.recurrence = lesson_bundle.build_recurrence(recurrence.WEEKLY)
    lesson_bundle.save()
    lesson.refresh_from_db()

    return lesson


@pytest.fixture
def supervision(time_grid):
    slot = BreakSlot.objects.create(
        time_grid=time_grid, weekday=0, time_start=time(10, 0), time_end=time(10, 15)
    )

    teachers = [
        Person.objects.create(first_name=f"supervision_{i}", last_name=f"{i}") for i in range(2)
    ]
    rooms = [
        Room.objects.create(name=f"supervision_{i}", short_name=f"supervision_{i}")
        for i in range(2)
    ]

    supervision = Supervision.objects.create(
        break_slot=slot,
    )
    supervision.recurrence = supervision.build_recurrence(recurrence.WEEKLY)
    supervision.save()
    supervision.teachers.set(teachers)
    supervision.rooms.set(rooms)

    return supervision


def test_sync_lesson(lesson):
    assert lesson.lesson_event is None

    bundle = lesson.bundle.first()
    bundle.sync()

    lesson.refresh_from_db()
    assert lesson.lesson_event

    lesson_event = lesson.lesson_event
    assert lesson_event.course == lesson.course
    assert lesson_event.subject == lesson.subject

    assert list(lesson_event.groups.all()) == list(lesson.course.groups.all())
    assert list(lesson_event.teachers.all()) == list(lesson.teachers.all())
    assert list(lesson.rooms.all()) == list(lesson.rooms.all())

    week_start = CalendarWeek.from_date(bundle.slot_start.time_grid.validity_range.date_start)
    datetime_start = bundle.slot_start.get_datetime_start(week_start)
    datetime_end = bundle.slot_end.get_datetime_end(week_start)

    assert lesson_event.datetime_start == datetime_start
    assert lesson_event.datetime_end == datetime_end

    assert lesson_event.recurrences == bundle.real_recurrence

    lesson.course = None
    lesson.save()
    bundle.sync()

    assert len(lesson.lesson_event.groups.all()) == 0


def test_sync_supervision(supervision):
    assert supervision.supervision_event is None

    supervision.sync()
    assert supervision.supervision_event

    supervision_event = supervision.supervision_event
    assert list(supervision_event.rooms.all()) == list(supervision.rooms.all())
    assert list(supervision_event.teachers.all()) == list(supervision.teachers.all())

    week_start = CalendarWeek.from_date(supervision.break_slot.time_grid.validity_range.date_start)
    datetime_start = supervision.break_slot.get_datetime_start(week_start)
    datetime_end = supervision.break_slot.get_datetime_end(week_start)

    assert supervision_event.datetime_start == datetime_start
    assert supervision_event.datetime_end == datetime_end

    assert supervision_event.recurrences == supervision.real_recurrence


def test_sync_on_publish(lesson, supervision):
    validity_range = lesson.bundle.first().slot_start.time_grid.validity_range
    validity_range.publish()

    lesson.refresh_from_db()
    supervision.refresh_from_db()

    assert lesson.lesson_event
    assert supervision.supervision_event


def test_sync_on_date_end_changed():
    pass


def test_sync_on_date_start_changed():
    pass


def test_sync_async(lesson, mocker, rf, admin_user):
    mock = mocker.patch("aleksis.apps.lesrooster.tasks.sync_validity_range.delay")
    mocker.patch("aleksis.apps.lesrooster.models.render_progress_page")

    request = rf.get("/")
    request.user = admin_user

    validity_range = lesson.bundle.first().slot_start.time_grid.validity_range

    validity_range.sync(request)

    assert not mock.called

    validity_range.status = ValidityRangeStatus.PUBLISHED
    validity_range.save()

    validity_range.sync(request)

    assert mock.called
