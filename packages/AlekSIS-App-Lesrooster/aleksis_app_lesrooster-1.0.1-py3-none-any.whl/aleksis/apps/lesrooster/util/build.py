from collections import OrderedDict
from typing import Union

from aleksis.apps.chronos.managers import TimetableType
from aleksis.apps.lesrooster.models import BreakSlot, Lesson, Slot, Supervision, TimeGrid
from aleksis.core.models import Group, Person, Room


def build_timetable(
    time_grid: TimeGrid,
    type_: TimetableType,
    obj: Union[Group, Room, Person],
) -> list | None:
    """Build regular timetable for the given time grid."""
    slots = Slot.objects.filter(time_grid=time_grid).order_by("weekday", "time_start")
    lesson_periods_per_slot = OrderedDict()
    supervisions_per_slot = OrderedDict()
    slot_map = OrderedDict()
    for slot in slots:
        lesson_periods_per_slot[slot] = []
        supervisions_per_slot[slot] = []
        slot_map.setdefault(slot.weekday, []).append(slot)

    max_slots_weekday, max_slots = max(slot_map.items(), key=lambda x: len(x[1]))
    max_slots = len(max_slots)

    # Get matching lessons
    lessons = Lesson.objects.filter(bundle__slot_start__time_grid=time_grid).filter_from_type(
        type_, obj
    )

    # Sort lesson periods in a dict
    for lesson in lessons:
        lesson_periods_per_slot[lesson.bundle.all()[0].slot_start].append(lesson)

    # Get matching supervisions
    supervisions = Supervision.objects.filter(break_slot__time_grid=time_grid).filter_from_type(
        type_, obj
    )

    for supervision in supervisions:
        supervisions_per_slot[supervision.break_slot] = supervision

    rows = []
    for slot_idx in range(max_slots):  # period is period after break
        left_slot = slot_map[max_slots_weekday][slot_idx]

        if isinstance(left_slot, BreakSlot):
            row = {"type": "break", "slot": left_slot}
        else:
            row = {
                "type": "period",
                "slot": left_slot,
            }

        cols = []

        for weekday in range(time_grid.weekday_min, time_grid.weekday_max + 1):
            if slot_idx > len(slot_map[weekday]) - 1:
                continue
            actual_slot = slot_map[weekday][slot_idx]

            if isinstance(actual_slot, BreakSlot):
                col = {"type": "break", "col": supervisions_per_slot.get(actual_slot)}

            else:
                col = {
                    "type": "period",
                    "col": (lesson_periods_per_slot.get(actual_slot, [])),
                }

            cols.append(col)

        row["cols"] = cols
        rows.append(row)

    return rows
