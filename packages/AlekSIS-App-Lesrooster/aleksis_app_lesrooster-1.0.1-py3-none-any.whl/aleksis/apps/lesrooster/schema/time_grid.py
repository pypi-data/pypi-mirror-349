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

from ..models import TimeGrid


class TimeGridType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    class Meta:
        model = TimeGrid
        fields = (
            "id",
            "validity_range",
            "group",
        )
        filter_fields = {
            "id": ["exact"],
            "group": ["exact", "in"],
            "validity_range": ["exact", "in"],
            "validity_range__date_start": ["exact", "lt", "lte", "gt", "gte"],
            "validity_range__date_end": ["exact", "lt", "lte", "gt", "gte"],
        }


class TimeGridBatchCreateMutation(DjangoBatchCreateMutation):
    class Meta:
        model = TimeGrid
        permissions = ("lesrooster.create_timegrid_rule",)
        only_fields = (
            "id",
            "validity_range",
            "group",
        )


class TimeGridBatchDeleteMutation(PermissionBatchDeleteMixin, DjangoBatchDeleteMutation):
    class Meta:
        model = TimeGrid
        permissions = ("lesrooster.delete_timegrid_rule",)


class TimeGridBatchPatchMutation(PermissionBatchPatchMixin, DjangoBatchPatchMutation):
    class Meta:
        model = TimeGrid
        permissions = ("lesrooster.edit_timegrid_rule",)
        only_fields = (
            "id",
            "validity_range",
            "group",
        )
