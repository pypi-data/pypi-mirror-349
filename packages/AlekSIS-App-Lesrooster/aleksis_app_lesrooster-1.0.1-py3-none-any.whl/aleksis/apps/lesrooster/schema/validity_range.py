from django.core.exceptions import PermissionDenied, ValidationError
from django.utils.translation import gettext_lazy as _

import graphene
from graphene_django.types import DjangoObjectType

from aleksis.core.schema.base import (
    BaseBatchCreateMutation,
    BaseBatchDeleteMutation,
    BaseBatchPatchMutation,
    DjangoFilterMixin,
    PermissionsTypeMixin,
)
from aleksis.core.util.core_helpers import get_active_school_term

from ..models import ValidityRange


class ValidityRangeType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    is_current = graphene.Boolean()

    class Meta:
        model = ValidityRange
        fields = ("id", "school_term", "name", "date_start", "date_end", "status", "time_grids")
        filter_fields = {
            "id": ["exact"],
            "school_term": ["exact", "in"],
            "status": ["iexact"],
            "name": ["icontains", "exact"],
            "date_start": ["exact", "lt", "lte", "gt", "gte"],
            "date_end": ["exact", "lt", "lte", "gt", "gte"],
        }


class ValidityRangeBatchCreateMutation(BaseBatchCreateMutation):
    class Meta:
        model = ValidityRange
        permissions = ("lesrooster.create_validityrange_rule",)
        only_fields = (
            "id",
            "name",
            "date_start",
            "date_end",
            "time_grids",
        )

    @classmethod
    def before_mutate(cls, root, info, input):  # noqa: A002
        active_school_term = get_active_school_term(info.context)

        if active_school_term is None:
            raise ValidationError(_("There is no school term for the school structure."))

        for obj in input:  # noqa: A002
            obj["school_term"] = active_school_term.pk

        return input  # noqa: A002


class ValidityRangeBatchDeleteMutation(BaseBatchDeleteMutation):
    class Meta:
        model = ValidityRange
        permissions = ("lesrooster.delete_validityrange_rule",)


class ValidityRangeBatchPatchMutation(BaseBatchPatchMutation):
    @classmethod
    def before_save(cls, root, info, input, updated_objects):  # noqa: A002
        res = super().before_save(root, info, input, updated_objects)

        # Get changes and cache them for after_mutate
        cls._changes = {}
        for updated_obj in updated_objects:
            if updated_obj.published:
                cls._changes[updated_obj.id] = updated_obj.status_tracker.changed()
        return res

    @classmethod
    def after_mutate(cls, root, info, input, updated_objs, return_data):  # noqa: A002
        res = super().after_mutate(root, info, input, updated_objs, return_data)

        # Sync validity range if date end has been changed
        for updated_obj in updated_objs:
            if updated_obj.published and updated_obj.id in cls._changes:
                changes = cls._changes[updated_obj.id]
                if "date_end" in changes:
                    updated_obj.sync(request=info.context)
        del cls._changes

        return res

    class Meta:
        model = ValidityRange
        permissions = ("lesrooster.edit_validityrange_rule",)
        only_fields = (
            "id",
            "name",
            "date_start",
            "date_end",
            "time_grids",
        )


class PublishValidityRangeMutation(graphene.Mutation):
    # No batch mutation as publishing can only be done for one validity range

    class Arguments:
        id = graphene.ID()  # noqa

    validity_range = graphene.Field(ValidityRangeType)

    @classmethod
    def mutate(cls, root, info, id):  # noqa
        validity_range = ValidityRange.objects.get(pk=id)

        if (
            not info.context.user.has_perm("lesrooster.edit_validityrange_rule", validity_range)
            or validity_range.published
        ):
            raise PermissionDenied()
        validity_range.publish(request=info.context)

        return PublishValidityRangeMutation(validity_range=validity_range)
