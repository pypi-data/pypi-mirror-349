import graphene
from graphene_django.types import DjangoObjectType
from graphene_django_cud.mutations import (
    DjangoBatchCreateMutation,
    DjangoBatchDeleteMutation,
    DjangoBatchPatchMutation,
)
from recurrence import Recurrence, deserialize

from aleksis.core.schema.base import (
    DjangoFilterMixin,
    OptimisticResponseTypeMixin,
    PermissionBatchDeleteMixin,
    PermissionBatchPatchMixin,
    PermissionsTypeMixin,
)

from ..models import Lesson


class LessonType(
    PermissionsTypeMixin, DjangoFilterMixin, OptimisticResponseTypeMixin, DjangoObjectType
):
    class Meta:
        model = Lesson
        fields = ("id", "bundle", "course", "rooms", "teachers", "subject")
        filter_fields = {
            "id": ["exact"],
        }

    @staticmethod
    def resolve_subject(root, info):
        # Return subject of course if lesson has no explicit subject
        if root.subject is None:
            return root.course.subject
        else:
            return root.subject


class LessonBatchCreateMutation(DjangoBatchCreateMutation):
    class Meta:
        model = Lesson
        only_fields = (
            "id",
            "course",
            "slot_start",
            "slot_end",
            "rooms",
            "teachers",
            "subject",
            "recurrence",
        )
        field_types = {"recurrence": graphene.String()}
        permissions = ("lesrooster.create_lesson_rule",)

    @classmethod
    def handle_recurrence(cls, value: str, name, info) -> Recurrence:
        return deserialize(value)


class LessonBatchDeleteMutation(PermissionBatchDeleteMixin, DjangoBatchDeleteMutation):
    class Meta:
        model = Lesson
        permissions = ("lesrooster.delete_lesson_rule",)


class LessonBatchPatchMutation(PermissionBatchPatchMixin, DjangoBatchPatchMutation):
    class Meta:
        model = Lesson
        only_fields = (
            "id",
            "course",
            "slot_start",
            "slot_end",
            "rooms",
            "teachers",
            "subject",
            "recurrence",
        )
        field_types = {"recurrence": graphene.String()}
        permissions = ("lesrooster.edit_lesson_rule",)

    @classmethod
    def handle_recurrence(cls, value: str, name, info) -> Recurrence:
        return deserialize(value)
