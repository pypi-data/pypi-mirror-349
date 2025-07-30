import graphene
from graphene_django.types import DjangoObjectType
from graphene_django_cud.mutations import (
    DjangoBatchCreateMutation,
    DjangoBatchDeleteMutation,
    DjangoBatchPatchMutation,
)

from aleksis.core.schema.base import (
    DjangoFilterMixin,
    PermissionBatchDeleteMixin,
    PermissionBatchPatchMixin,
    PermissionsTypeMixin,
)

from ..models import BreakSlot
from .slot import slot_filters

break_filters = slot_filters.copy()


class BreakSlotType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    model = graphene.String(default_value="Break")

    class Meta:
        model = BreakSlot
        fields = (
            "id",
            "time_grid",
            "name",
            "weekday",
            "period",
            "time_start",
            "time_end",
        )
        filter_fields = break_filters


class BreakSlotBatchCreateMutation(PermissionBatchPatchMixin, DjangoBatchCreateMutation):
    class Meta:
        model = BreakSlot
        return_field_name = "breakSlots"
        field_types = {"weekday": graphene.Int()}
        only_fields = (
            "id",
            "time_grid",
            "name",
            "weekday",
            "period",
            "time_start",
            "time_end",
        )
        permissions = ("lesrooster.create_breakslot_rule",)


class BreakSlotBatchDeleteMutation(PermissionBatchDeleteMixin, DjangoBatchDeleteMutation):
    class Meta:
        model = BreakSlot
        permissions = ("lesrooster.delete_breakslot_rule",)


class BreakSlotBatchPatchMutation(PermissionBatchPatchMixin, DjangoBatchPatchMutation):
    class Meta:
        model = BreakSlot
        return_field_name = "breakSlots"
        field_types = {"weekday": graphene.Int()}
        permissions = ("lesrooster.edit_breakslot_rule",)
        only_fields = (
            "id",
            "time_grid",
            "name",
            "weekday",
            "period",
            "time_start",
            "time_end",
        )
