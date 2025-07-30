from django.db import migrations

from django.db.models import Q

def _create_tcc(apps, schema_editor):
    ValidityRange = apps.get_model("lesrooster", "ValidityRange")
    TimeboundCourseConfig = apps.get_model("lesrooster", "TimeboundCourseConfig")
    Course = apps.get_model("cursus", "Course")
    db_alias = schema_editor.connection.alias
    for validity_range in ValidityRange.objects.using(db_alias).all():
        # Duplicated from models.py TimeboundCourseConfig.create_for_validity_range
        # because the historical model used here does not have this method.
        for course in Course.objects.filter(
                Q(groups__school_term__pk=validity_range.school_term.pk) |
                Q(groups__parent_groups__school_term__pk=validity_range.school_term.pk)
        ):
            tcc, __ = TimeboundCourseConfig.objects.update_or_create(
                course=course,
                validity_range=validity_range,
                defaults=dict(managed_by_app_label=TimeboundCourseConfig._meta.app_label,
                lesson_quota=course.lesson_quota),
            )
            tcc.teachers.set(course.teachers.all())


class Migration(migrations.Migration):

    dependencies = [
        ('lesrooster', '0017_migrate_from_chronos'),
    ]

    operations = [
        migrations.RunPython(_create_tcc),
    ]
