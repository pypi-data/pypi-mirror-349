from datetime import date, timedelta

from django.core.exceptions import ValidationError

import pytest
from freezegun import freeze_time

from aleksis.apps.lesrooster.models import TimeGrid, ValidityRange, ValidityRangeStatus
from aleksis.core.models import SchoolTerm

pytestmark = pytest.mark.django_db


def test_create_default_time_grid():
    date_start = date(2024, 1, 1)
    date_end = date(2024, 6, 1)

    school_term = SchoolTerm.objects.create(name="Test", date_start=date_start, date_end=date_end)

    validity_range = ValidityRange.objects.create(
        school_term=school_term, date_start=date_start, date_end=date_end
    )

    assert TimeGrid.objects.filter(validity_range=validity_range, group=None).exists()


def test_current_validity_range():
    date_start = date(2024, 1, 1)
    date_end = date(2024, 6, 1)

    school_term = SchoolTerm.objects.create(name="Test", date_start=date_start, date_end=date_end)

    validity_range = ValidityRange.objects.create(
        school_term=school_term, date_start=date_start, date_end=date_end
    )

    assert ValidityRange.get_current(date_end) == validity_range
    assert ValidityRange.get_current(date_end + timedelta(days=1)) is None

    with freeze_time(date_start):
        assert ValidityRange.current == validity_range
        assert validity_range.is_current

    with freeze_time(date_end + timedelta(days=1)):
        assert ValidityRange.current is None
        assert not validity_range.is_current


def test_validity_range_date_start_before_date_end():
    date_start = date(2024, 1, 2)
    date_end = date(2024, 1, 1)

    school_term = SchoolTerm.objects.create(name="Test", date_start=date_start, date_end=date_end)

    validity_range = ValidityRange(
        school_term=school_term, date_start=date_start, date_end=date_end
    )
    with pytest.raises(
        ValidationError, match=r".*The start date must be earlier than the end date\..*"
    ):
        validity_range.full_clean()


def test_validity_range_within_school_term():
    date_start = date(2024, 1, 1)
    date_end = date(2024, 6, 1)
    school_term = SchoolTerm.objects.create(name="Test", date_start=date_start, date_end=date_end)

    dates_fail = [
        (date_start - timedelta(days=1), date_end),
        (date_start, date_end + timedelta(days=1)),
        (date_start - timedelta(days=1), date_end + timedelta(days=1)),
    ]

    dates_success = [
        (date_start, date_end),
        (date_start + timedelta(days=1), date_end),
        (date_start, date_end - timedelta(days=1)),
        (date_start + timedelta(days=1), date_end - timedelta(days=1)),
    ]

    for d_start, d_end in dates_fail:
        validity_range = ValidityRange(school_term=school_term, date_start=d_start, date_end=d_end)
        with pytest.raises(
            ValidationError, match=r".*The validity range must be within the school term\..*"
        ):
            validity_range.full_clean()

    for d_start, d_end in dates_success:
        validity_range = ValidityRange(school_term=school_term, date_start=d_start, date_end=d_end)
        validity_range.full_clean()


def test_validity_range_overlaps():
    date_start = date(2024, 1, 1)
    date_end = date(2024, 6, 1)
    school_term = SchoolTerm.objects.create(name="Test", date_start=date_start, date_end=date_end)

    validity_range_1 = ValidityRange.objects.create(
        date_start=date_start + timedelta(days=10),
        date_end=date_end - timedelta(days=10),
        school_term=school_term,
        status=ValidityRangeStatus.PUBLISHED,
    )

    dates_fail = [
        (date_start, validity_range_1.date_start),
        (date_start, date_end),
        (date_start, validity_range_1.date_end),
        (validity_range_1.date_start, validity_range_1.date_end),
        (validity_range_1.date_end, date_end),
    ]

    for d_start, d_end in dates_fail:
        validity_range_2 = ValidityRange.objects.create(
            date_start=d_start, date_end=d_end, school_term=school_term
        )
        with pytest.raises(
            ValidationError,
            match=r".*There is already a published validity range "
            r"for this time or a part of this time\..*",
        ):
            validity_range_2.publish()


def test_change_published_validity_range():
    date_start = date(2024, 1, 1)
    date_end = date(2024, 6, 1)
    school_term = SchoolTerm.objects.create(
        name="Test",
        date_start=date_start - timedelta(days=5),
        date_end=date_end + timedelta(days=5),
    )
    school_term_2 = SchoolTerm.objects.create(
        name="Test 2",
        date_start=date_end + timedelta(days=6),
        date_end=date_end + timedelta(days=7),
    )

    validity_range = ValidityRange.objects.create(
        date_start=date_start,
        date_end=date_end,
        school_term=school_term,
        status=ValidityRangeStatus.PUBLISHED,
    )

    # School term
    validity_range.refresh_from_db()
    validity_range.school_term = school_term_2
    with pytest.raises(ValidationError):
        validity_range.full_clean()

    # Name
    validity_range.refresh_from_db()
    validity_range.name = "Test"
    validity_range.full_clean()

    # Status
    validity_range.refresh_from_db()
    validity_range.status = ValidityRangeStatus.DRAFT
    with pytest.raises(ValidationError):
        validity_range.full_clean()

    with freeze_time(date_start - timedelta(days=1)):  # current date start is in the future
        # Date start in the past
        validity_range.refresh_from_db()
        validity_range.date_start = validity_range.date_start - timedelta(days=2)
        with pytest.raises(
            ValidationError, match=r".*You can't set the start date to a date in the past.*"
        ):
            validity_range.full_clean()

        # Date start today
        validity_range.refresh_from_db()
        validity_range.date_start = validity_range.date_start - timedelta(days=1)
        validity_range.full_clean()

        # Date start in the future
        validity_range.refresh_from_db()
        validity_range.date_start = validity_range.date_start + timedelta(days=2)
        validity_range.full_clean()

    with freeze_time(date_start + timedelta(days=1)):  # current date start is in the past
        # Date start in the past
        validity_range.refresh_from_db()
        validity_range.date_start = validity_range.date_start - timedelta(days=2)
        with pytest.raises(
            ValidationError,
            match=r".*You can't change the start date if the validity range is already active.*",
        ):
            validity_range.full_clean()

        # Date start in the future
        validity_range.refresh_from_db()
        validity_range.date_start = validity_range.date_start + timedelta(days=2)
        with pytest.raises(
            ValidationError,
            match=r".*You can't change the start date if the validity range is already active.*",
        ):
            validity_range.full_clean()

    with freeze_time(date_end - timedelta(days=3)):  # current date end is in the future
        # Date end in the past
        validity_range.refresh_from_db()
        validity_range.date_end = validity_range.date_end - timedelta(days=4)
        with pytest.raises(
            ValidationError,
            match=r".*To avoid data loss, the validity range "
            r"can be only shortened until the current day.*",
        ):
            validity_range.full_clean()

        # Date end today
        validity_range.refresh_from_db()
        validity_range.date_end = validity_range.date_end - timedelta(days=3)
        validity_range.full_clean()

        # Date end in the future
        validity_range.refresh_from_db()
        validity_range.date_end = validity_range.date_end - timedelta(days=2)
        validity_range.full_clean()

    with freeze_time(date_end + timedelta(days=1)):  # current date end is in the past
        validity_range.refresh_from_db()
        validity_range.date_end = validity_range.date_end - timedelta(days=2)
        with pytest.raises(
            ValidationError,
            match=r".*You can't change the end date if the validity range is already in the past.*",
        ):
            validity_range.full_clean()


# TODO Test sync with date change
