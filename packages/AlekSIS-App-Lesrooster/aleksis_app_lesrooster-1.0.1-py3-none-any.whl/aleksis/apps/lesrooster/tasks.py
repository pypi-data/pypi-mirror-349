from aleksis.core.util.celery_progress import ProgressRecorder, recorded_task


@recorded_task
def sync_validity_range(validity_range: int, recorder: ProgressRecorder):
    """Sync all lessons and supervisions of this validity range."""
    from .models import ValidityRange

    validity_range = ValidityRange.objects.get(pk=validity_range)

    validity_range._sync(recorder=recorder)
