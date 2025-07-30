from collections.abc import Iterable
from datetime import time
from typing import Optional, Union

from django.db.models import Max, Min, Q, QuerySet
from django.db.models.functions import Coalesce

from polymorphic.query import PolymorphicQuerySet

from aleksis.apps.chronos.managers import TimetableType
from aleksis.core.managers import (
    AlekSISBaseManagerWithoutMigrations,
    DateRangeQuerySetMixin,
    PolymorphicBaseManager,
)
from aleksis.core.models import Group, Person, Room


class TeacherPropertiesMixin:
    """Mixin for common teacher properties.

    Necessary method: `get_teachers`
    """

    def get_teacher_names(self, sep: Optional[str] = ", ") -> str:
        return sep.join([teacher.full_name for teacher in self.get_teachers()])

    @property
    def teacher_names(self) -> str:
        return self.get_teacher_names()

    def get_teacher_short_names(self, sep: str = ", ") -> str:
        return sep.join([teacher.short_name for teacher in self.get_teachers()])

    @property
    def teacher_short_names(self) -> str:
        return self.get_teacher_short_names()


class RoomPropertiesMixin:
    """Mixin for common room properties.

    Necessary method: `get_rooms`
    """

    def get_room_names(self, sep: Optional[str] = ", ") -> str:
        return sep.join([room.name for room in self.get_rooms()])

    @property
    def room_names(self) -> str:
        return self.get_room_names()

    def get_room_short_names(self, sep: str = ", ") -> str:
        return sep.join([room.short_name for room in self.get_rooms()])

    @property
    def room_short_names(self) -> str:
        return self.get_room_short_names()


class ValidityRangeQuerySet(QuerySet, DateRangeQuerySetMixin):
    """Custom query set for validity ranges."""


class ValidityRangeManager(AlekSISBaseManagerWithoutMigrations):
    """Manager for validity ranges."""


class SlotQuerySet(PolymorphicQuerySet):
    def get_period_min(self) -> int:
        """Get minimum period."""
        return self.aggregate(period__min=Coalesce(Min("period"), 1)).get("period__min")

    def get_period_max(self) -> int:
        """Get maximum period."""
        return self.aggregate(period__max=Coalesce(Max("period"), 7)).get("period__max")

    def get_time_min(self) -> time | None:
        """Get minimum time."""
        return self.aggregate(Min("time_start")).get("time_start__min")

    def get_time_max(self) -> time | None:
        """Get maximum time."""
        return self.aggregate(Max("time_end")).get("time_end__max")

    def get_weekday_min(self) -> int:
        """Get minimum weekday."""
        return self.aggregate(weekday__min=Coalesce(Min("weekday"), 0)).get("weekday__min")

    def get_weekday_max(self) -> int:
        """Get maximum weekday."""
        return self.aggregate(weekday__max=Coalesce(Max("weekday"), 6)).get("weekday__max")


class SlotManager(PolymorphicBaseManager):
    pass


class LessonQuerySet(QuerySet):
    def filter_participant(self, person: Union[Person, int]) -> "LessonQuerySet":
        """Filter for all lessons a participant (student) attends."""
        return self.filter(course__groups__members=person)

    def filter_group(self, group: Union[Group, int]) -> "LessonQuerySet":
        """Filter for all lessons a group (class) regularly attends."""
        if isinstance(group, int):
            group = Group.objects.get(pk=group)

        return self.filter(
            Q(course__groups=group) | Q(course__groups__parent_groups=group)
        ).distinct()

    def filter_groups(self, groups: Iterable[Group]) -> "LessonQuerySet":
        """Filter for all lessons one of the groups regularly attends."""
        return self.filter(
            Q(course__groups__in=groups) | Q(course__groups__parent_groups__in=groups)
        )

    def filter_teacher(self, teacher: Union[Person, int]) -> "LessonQuerySet":
        """Filter for all lessons given by a certain teacher."""
        return self.filter(teachers=teacher)

    def filter_room(self, room: Union[Room, int]) -> "LessonQuerySet":
        """Filter for all lessons taking part in a certain room."""
        return self.filter(rooms=room)

    def filter_from_type(
        self,
        type_: TimetableType,
        obj: Union[Person, Group, Room, int],
    ) -> "LessonQuerySet":
        """Filter lessons for a group, teacher or room by provided type."""
        if type_ == TimetableType.GROUP:
            return self.filter_group(obj)
        elif type_ == TimetableType.TEACHER:
            return self.filter_teacher(obj)
        elif type_ == TimetableType.ROOM:
            return self.filter_room(obj)
        else:
            return self.none()

    def filter_from_person(self, person: Person) -> "LessonQuerySet":
        """Filter lessons for a person."""
        type_ = person.timetable_type

        if type_ == TimetableType.TEACHER:
            return self.filter_teacher(person)
        elif type_ == TimetableType.GROUP:
            return self.filter_participant(person)
        else:
            return self.none()


class LessonManager(AlekSISBaseManagerWithoutMigrations):
    pass


class SupervisionQuerySet(QuerySet):
    def filter_teacher(self, teacher: Union[Person, int]) -> "SupervisionQuerySet":
        """Filter for all supervisions done by a certain teacher."""
        return self.filter(teachers=teacher)

    def filter_room(self, room: Union[Room, int]) -> "SupervisionQuerySet":
        """Filter for all supervisions taking part in a certain room."""
        return self.filter(rooms=room)

    def filter_from_type(
        self,
        type_: TimetableType,
        obj: Union[Person, Group, Room, int],
    ) -> "SupervisionQuerySet":
        """Filter supervisions for a eacher or room by provided type."""
        if type_ == TimetableType.TEACHER:
            return self.filter_teacher(obj)
        elif type_ == TimetableType.ROOM:
            return self.filter_room(obj)
        else:
            return self.none()

    def filter_from_person(self, person: Person) -> Optional["SupervisionQuerySet"]:
        """Filter supervisions for a person."""

        return self.filter_teacher(person)


class SupervisionManager(AlekSISBaseManagerWithoutMigrations):
    pass
