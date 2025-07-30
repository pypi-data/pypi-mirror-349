from django.apps import apps
from django.db.models import Model
from django.utils.translation import gettext as _

import recurrence

from .models import Lesson, Slot, ValidityRange

if apps.is_installed("aleksis.apps.csv_import"):
    from aleksis.apps.csv_import.field_types import ProcessFieldType

    class SlotByDayAndPeriodFieldType(ProcessFieldType):
        _class_name = "slot_by_day_and_period"
        verbose_name = _("Slot by day (1-7) and period")
        run_before_save = True

        def process(self, instance: Model, value):
            validity_range = int(self.additional_params["validity_range"])
            validity_range = ValidityRange.objects.get(id=validity_range)
            day, period = value.split("-")
            day = int(day) - 1
            period = int(period)
            slot = Slot.objects.get(
                time_grid__validity_range=validity_range,
                time_grid__group=None,
                weekday=day,
                period=period,
            )
            instance.slot_start = slot
            instance.slot_end = slot

    class WeeklyRecurrenceFieldType(ProcessFieldType):
        _class_name = "weekly_recurrence"
        verbose_name = _("Weekly recurrence (for lessons, supervisions etc.)")

        def process(self, instance: Model, value):
            instance.recurrence = instance.build_recurrence(recurrence.WEEKLY)
            instance.save()

    class LessonForBundleByUniqueReferenceFieldType(ProcessFieldType):
        _class_name = "lesson_for_bundle_by_unique_reference"
        verbose_name = _("Lesson for lesson bundle by unique reference")

        def process(self, instance: Model, value):
            lesson = Lesson.objects.get(extended_data__import_ref_csv=value)
            instance.lessons.set([lesson])
