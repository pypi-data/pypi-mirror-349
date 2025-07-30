import graphene
from graphene_django.types import DjangoObjectType
from graphene_django_cud.mutations import (
    DjangoBatchCreateMutation,
    DjangoBatchDeleteMutation,
    DjangoBatchPatchMutation,
)
from recurrence import Recurrence, deserialize, serialize

from aleksis.core.schema.base import (
    DjangoFilterMixin,
    OptimisticResponseTypeMixin,
    PermissionBatchDeleteMixin,
    PermissionBatchPatchMixin,
    PermissionsTypeMixin,
)

from ..models import Lesson, LessonBundle
from .timebound_course_bundle import TimeboundCourseBundleType


class LessonBundleType(
    PermissionsTypeMixin, DjangoFilterMixin, OptimisticResponseTypeMixin, DjangoObjectType
):
    class Meta:
        model = LessonBundle
        fields = ("id", "lessons", "slot_start", "slot_end")
        filter_fields = {
            "id": ["exact"],
            "slot_start": ["exact"],
            "slot_end": ["exact"],
        }

    recurrence = graphene.String()
    course_bundle = graphene.Field(TimeboundCourseBundleType)

    @staticmethod
    def resolve_recurrence(root, info, **kwargs):
        return serialize(root.recurrence)

    @staticmethod
    def resolve_course_bundle(root, info, **kwargs):
        return root.course_bundle


class LessonBundleBatchCreateMutation(DjangoBatchCreateMutation):
    class Meta:
        model = LessonBundle
        only_fields = ("id", "slot_start", "slot_end", "recurrence", "course_bundle")
        field_types = {"recurrence": graphene.String()}
        permissions = ("lesrooster.create_lesson_bundle_rule",)

    @classmethod
    def handle_recurrence(cls, value: str, name, info) -> Recurrence:
        return deserialize(value)

    @classmethod
    def before_save(cls, root, info, input, created_objects):  # noqa
        """Create and add lessons."""
        for lesson_bundle in created_objects:
            validity_range = lesson_bundle.slot_start.time_grid.validity_range
            lesson_bundle.lessons.set(
                [
                    Lesson.create_from_course(course, validity_range)
                    for course in lesson_bundle.course_bundle.courses.all()
                ]
            )

        return created_objects


class LessonBundleBatchPatchMutation(PermissionBatchPatchMixin, DjangoBatchPatchMutation):
    class Meta:
        model = LessonBundle
        only_fields = (
            "id",
            "course_bundle",
            "lessons",
            "slot_start",
            "slot_end",
            "recurrence",
        )
        field_types = {"recurrence": graphene.String()}
        permissions = ("lesrooster.edit_lesson_bundle_rule",)

    @classmethod
    def handle_recurrence(cls, value: str, name, info) -> Recurrence:
        return deserialize(value)


class LessonBundleBatchDeleteMutation(PermissionBatchDeleteMixin, DjangoBatchDeleteMutation):
    class Meta:
        model = LessonBundle
        permissions = ("lesrooster.delete_lesson_bundle_rule",)
