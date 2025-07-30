from django.db.models import Prefetch, Q, Value

import graphene
import graphene_django_optimizer
from guardian.shortcuts import get_objects_for_user

from aleksis.apps.chronos.schema import TimetableGroupType
from aleksis.apps.cursus.models import Course, CourseBundle, Subject
from aleksis.core.models import Group
from aleksis.core.schema.base import FilterOrderList
from aleksis.core.schema.group import GroupType
from aleksis.core.util.core_helpers import filter_active_school_term, get_site_preferences

from ..models import (
    BreakSlot,
    Lesson,
    LessonBundle,
    Slot,
    Supervision,
    TimeboundCourseConfig,
    TimeGrid,
    ValidityRange,
)
from .break_slot import (
    BreakSlotBatchCreateMutation,
    BreakSlotBatchDeleteMutation,
    BreakSlotBatchPatchMutation,
    BreakSlotType,
)
from .lesson import (
    LessonBatchPatchMutation,
    LessonType,
)
from .lesson_bundle import (
    LessonBundleBatchCreateMutation,
    LessonBundleBatchDeleteMutation,
    LessonBundleBatchPatchMutation,
    LessonBundleType,
)
from .slot import (
    CarryOverSlotsMutation,
    CopySlotsFromDifferentTimeGridMutation,
    SlotBatchCreateMutation,
    SlotBatchDeleteMutation,
    SlotBatchPatchMutation,
    SlotType,
)
from .supervision import (
    SupervisionBatchCreateMutation,
    SupervisionBatchDeleteMutation,
    SupervisionBatchPatchMutation,
    SupervisionType,
)
from .time_grid import (
    TimeGridBatchCreateMutation,
    TimeGridBatchDeleteMutation,
    TimeGridType,
)
from .timebound_course_bundle import TimeboundCourseBundleType
from .timebound_course_config import (
    CourseBatchCreateForValidityRangeMutation,
    LesroosterExtendedSubjectType,
    TimeboundCourseConfigBatchCreateMutation,
    TimeboundCourseConfigBatchDeleteMutation,
    TimeboundCourseConfigBatchPatchMutation,
    TimeboundCourseConfigType,
)
from .validity_range import (
    PublishValidityRangeMutation,
    ValidityRangeBatchCreateMutation,
    ValidityRangeBatchDeleteMutation,
    ValidityRangeBatchPatchMutation,
    ValidityRangeType,
)


class Query(graphene.ObjectType):
    break_slots = FilterOrderList(BreakSlotType)
    slots = FilterOrderList(SlotType)
    timebound_course_configs = FilterOrderList(TimeboundCourseConfigType)
    validity_ranges = FilterOrderList(ValidityRangeType)
    time_grids = FilterOrderList(TimeGridType)
    lessons = FilterOrderList(LessonType)
    supervisions = FilterOrderList(SupervisionType)

    groups_for_planning = graphene.List(TimetableGroupType)
    course_bundles_for_group = graphene.List(
        TimeboundCourseBundleType,
        group=graphene.ID(required=True),
        validity_range=graphene.ID(required=True),
    )
    lesson_bundles_for_group = graphene.List(
        LessonBundleType,
        group=graphene.ID(required=True),
        time_grid=graphene.ID(required=True),
    )
    lesson_bundles_for_rooms_or_teachers = graphene.List(
        LessonBundleType,
        rooms=graphene.List(graphene.ID, required=True),
        teachers=graphene.List(graphene.ID, required=True),
        time_grid=graphene.ID(required=True),
    )
    lessons_for_group = graphene.List(
        LessonType,
        group=graphene.ID(required=True),
        time_grid=graphene.ID(required=True),
    )
    lessons_for_teacher = graphene.List(
        LessonType,
        teacher=graphene.ID(required=True),
        time_grid=graphene.ID(required=True),
    )
    lessons_for_room = graphene.List(
        LessonType,
        room=graphene.ID(required=True),
        time_grid=graphene.ID(required=True),
    )

    lessons_for_rooms_or_teachers = graphene.List(
        LessonType,
        rooms=graphene.List(graphene.ID, required=True),
        teachers=graphene.List(graphene.ID, required=True),
        time_grid=graphene.ID(required=True),
    )

    current_validity_range = graphene.Field(ValidityRangeType)
    validity_range_by_id = graphene.Field(ValidityRangeType, id=graphene.ID())

    lesrooster_extended_subjects = FilterOrderList(
        LesroosterExtendedSubjectType,
        groups=graphene.List(graphene.ID),
        include_child_groups=graphene.Boolean(required=True),
    )

    groups_by_time_grid = graphene.List(GroupType, time_grid=graphene.ID(required=True))

    @staticmethod
    def resolve_break_slots(root, info):
        qs = filter_active_school_term(
            info.context, BreakSlot.objects.all(), "time_grid__validity_range__school_term"
        )
        if not info.context.user.has_perm("lesrooster.view_breakslot_rule"):
            return graphene_django_optimizer.query(
                get_objects_for_user(info.context.user, "lesrooster.view_breakslot", qs), info
            )
        return graphene_django_optimizer.query(qs, info)

    @staticmethod
    def resolve_slots(root, info):
        # Note: This does also return `Break` objects (but with type set to Slot). This is intended
        slots = Slot.objects.non_polymorphic()
        slots = filter_active_school_term(
            info.context, slots, "time_grid__validity_range__school_term"
        )
        if not info.context.user.has_perm("lesrooster.view_slot_rule"):
            return graphene_django_optimizer.query(
                get_objects_for_user(info.context.user, "lesrooster.view_slot", slots), info
            )
        return graphene_django_optimizer.query(slots, info)

    @staticmethod
    def resolve_timebound_course_configs(root, info):
        tccs = filter_active_school_term(
            info.context, TimeboundCourseConfig.objects.all(), "validity_range__school_term"
        )
        if not info.context.user.has_perm("lesrooster.view_timeboundcourseconfig_rule"):
            return graphene_django_optimizer.query(
                get_objects_for_user(
                    info.context.user, "lesrooster.view_timeboundcourseconfig", tccs
                ),
                info,
            )
        return graphene_django_optimizer.query(tccs, info)

    @staticmethod
    def resolve_validity_ranges(root, info):
        qs = filter_active_school_term(info.context, ValidityRange.objects.all())
        if not info.context.user.has_perm("lesrooster.view_validityrange_rule"):
            return graphene_django_optimizer.query(
                get_objects_for_user(info.context.user, "lesrooster.view_validityrange", qs), info
            )
        return graphene_django_optimizer.query(qs, info)

    @staticmethod
    def resolve_time_grids(root, info):
        qs = filter_active_school_term(
            info.context, TimeGrid.objects.all(), "validity_range__school_term"
        ).order_by("-validity_range__date_start")
        if not info.context.user.has_perm("lesrooster.view_timegrid_rule"):
            return graphene_django_optimizer.query(
                get_objects_for_user(info.context.user, "lesrooster.view_timegrid", qs), info
            )
        return graphene_django_optimizer.query(qs, info)

    @staticmethod
    def resolve_supervisions(root, info):
        qs = filter_active_school_term(
            info.context,
            Supervision.objects.all(),
            "break_slot__time_grid__validity_range__school_term",
        )
        if not info.context.user.has_perm("lesrooster.view_supervision_rule"):
            return graphene_django_optimizer.query(
                get_objects_for_user(info.context.user, "lesrooster.view_supervision", qs), info
            )
        return graphene_django_optimizer.query(qs, info)

    @staticmethod
    def resolve_lesrooster_extended_subjects(root, info, groups, include_child_groups):
        if include_child_groups:
            courses = Course.objects.filter(
                Q(groups__in=groups) | Q(groups__parent_groups__in=groups)
            )
        else:
            courses = Course.objects.filter(groups__in=groups)

        course_configs = filter_active_school_term(
            info.context,
            TimeboundCourseConfig.objects.all(),
            "validity_range__school_term",
        )
        if not info.context.user.has_perm("lesrooster.view_timeboundcourseconfig_rule"):
            course_configs = get_objects_for_user(
                info.context.user,
                "lesrooster.view_timeboundcourseconfig",
                course_configs,
            )

        subjects = Subject.objects.all().prefetch_related(
            Prefetch(
                "courses",
                queryset=get_objects_for_user(
                    info.context.user,
                    "cursus.view_course",
                    courses.prefetch_related(
                        Prefetch("lr_timebound_course_configs", queryset=course_configs)
                    ),
                ),
            )
        )

        if not info.context.user.has_perm("lesrooster.view_subject_rule"):
            return graphene_django_optimizer.query(
                get_objects_for_user(info.context.user, "cursus.view_subject", subjects), info
            )
        return graphene_django_optimizer.query(subjects, info)

    @staticmethod
    def resolve_current_validity_range(root, info):
        validity_range = ValidityRange.current
        if info.context.user.has_perm("lesrooster.view_validityrange_rule", validity_range):
            return validity_range

    @staticmethod
    def resolve_validity_range_by_id(root, info, id):  # noqa: A002
        validity_range = ValidityRange.objects.get(id=id)
        if info.context.user.has_perm("lesrooster.view_validityrange_rule", validity_range):
            return validity_range

    @staticmethod
    def resolve_groups_for_planning(root, info):
        if not info.context.user.has_perm("lesrooster.plan_timetables_rule"):
            return []
        groups = filter_active_school_term(info.context, Group.objects.all())
        group_types = get_site_preferences()["chronos__group_types_timetables"]

        if group_types:
            groups = groups.filter(group_type__in=group_types)

        return graphene_django_optimizer.query(groups, info)

    def resolve_course_bundles_for_group(root, info, group, validity_range):
        """Get all course_bundles for group & validity_range."""

        # The validity_range is used to lookup the timebound_course_config.

        # The argument could be time_grid aswell since it is group &
        # validity_range but then the backend has to lookup what the
        # frontend already knows.

        if not info.context.user.has_perm("lesrooster.plan_timetables_rule"):
            return []

        return graphene_django_optimizer.query(
            CourseBundle.objects.filter(
                Q(courses__groups__id=group) | Q(courses__groups__parent_groups__id=group)
            )
            .distinct()
            .annotate(validity_range_id=Value(validity_range)),
            info,
        )

    def resolve_lesson_bundles_for_group(root, info, group, time_grid):
        """Get all lesson_bundles for group & validity_range."""
        if not info.context.user.has_perm("lesrooster.plan_timetables_rule"):
            return []

        return LessonBundle.objects.filter(
            Q(lessons__course__groups__id=group)
            | Q(lessons__course__groups__parent_groups__id=group),
            slot_start__time_grid_id=time_grid,
            slot_end__time_grid_id=time_grid,
        ).distinct()

    @staticmethod
    def resolve_lesson_bundles_for_rooms_or_teachers(
        root, info, time_grid, rooms=None, teachers=None
    ):
        if teachers is None:
            teachers = []
        if rooms is None:
            rooms = []
        if not info.context.user.has_perm("lesrooster.plan_timetables_rule"):
            return []

        return graphene_django_optimizer.query(
            LessonBundle.objects.filter(
                Q(lessons__rooms__in=rooms) | Q(lessons__teachers__in=teachers),
                slot_start__time_grid_id=time_grid,
                slot_end__time_grid_id=time_grid,
            ).distinct(),
            info,
        )

    @staticmethod
    def resolve_lessons_for_group(root, info, group, time_grid):
        if not info.context.user.has_perm("lesrooster.plan_timetables_rule"):
            return []

        group = Group.objects.get(pk=group)

        if not group:
            return []

        courses = Course.objects.filter(Q(groups__in=group.child_groups.all()) | Q(groups=group))

        return graphene_django_optimizer.query(
            Lesson.objects.filter(
                course__in=courses,
                bundle__slot_start__time_grid_id=time_grid,
                bundle__slot_end__time_grid_id=time_grid,
            ),
            info,
        )

    @staticmethod
    def resolve_lessons_for_teacher(root, info, teacher, time_grid):
        if not info.context.user.has_perm("lesrooster.plan_timetables_rule"):
            return []

        return graphene_django_optimizer.query(
            Lesson.objects.filter(
                teachers=teacher,
                bundle__slot_start__time_grid_id=time_grid,
                bundle__slot_end__time_grid_id=time_grid,
            ).distinct(),
            info,
        )

    @staticmethod
    def resolve_lessons_for_room(root, info, room, time_grid):
        if not info.context.user.has_perm("lesrooster.plan_timetables_rule"):
            return []

        return graphene_django_optimizer.query(
            Lesson.objects.filter(
                rooms=room,
                bundle__slot_start__time_grid_id=time_grid,
                bundle__slot_end__time_grid_id=time_grid,
            ).distinct(),
            info,
        )

    @staticmethod
    def resolve_lessons_objects_for_rooms_or_teachers(
        root, info, time_grid, rooms=None, teachers=None
    ):
        if teachers is None:
            teachers = []
        if rooms is None:
            rooms = []
        if not info.context.user.has_perm("lesrooster.plan_timetables_rule"):
            return []

        return graphene_django_optimizer.query(
            Lesson.objects.filter(
                Q(rooms__in=rooms) | Q(teachers__in=teachers),
                bundle__slot_start__time_grid_id=time_grid,
                bundle__slot_end__time_grid_id=time_grid,
            ).distinct(),
            info,
        )

    @staticmethod
    def resolve_groups_by_time_grid(root, info, time_grid=None, **kwargs):
        if not info.context.user.has_perm("lesrooster.plan_timetables_rule"):
            return []

        # This will fail if the ID is invalid, but won't, if it is empty
        time_grid_obj: TimeGrid | None = (
            TimeGrid.objects.get(pk=time_grid) if time_grid is not None else None
        )

        # If there is no time_grid, or it is a generic one, filter groups
        # to have a fitting school_term
        if time_grid_obj is None or time_grid_obj.group is None:
            return (
                filter_active_school_term(info.context, Group.objects.all())
                .annotate(has_cg=Q(child_groups__isnull=False))
                .order_by("-has_cg", "name")
            )

        group_id = time_grid_obj.group.pk

        return graphene_django_optimizer.query(
            Group.objects.filter(
                Q(pk=group_id)
                | Q(parent_groups=group_id)
                | Q(parent_groups__parent_groups=group_id)
            )
            .distinct()
            .annotate(has_cg=Q(child_groups__isnull=False))
            .order_by("-has_cg", "name"),
            info,
        )


class Mutation(graphene.ObjectType):
    create_break_slots = BreakSlotBatchCreateMutation.Field()
    delete_break_slots = BreakSlotBatchDeleteMutation.Field()
    update_break_slots = BreakSlotBatchPatchMutation.Field()

    create_slots = SlotBatchCreateMutation.Field()
    delete_slots = SlotBatchDeleteMutation.Field()
    update_slots = SlotBatchPatchMutation.Field()

    create_timebound_course_configs = TimeboundCourseConfigBatchCreateMutation.Field()
    delete_timebound_course_configs = TimeboundCourseConfigBatchDeleteMutation.Field()
    update_timebound_course_configs = TimeboundCourseConfigBatchPatchMutation.Field()
    carry_over_slots = CarryOverSlotsMutation.Field()
    copy_slots_from_grid = CopySlotsFromDifferentTimeGridMutation.Field()

    create_validity_ranges = ValidityRangeBatchCreateMutation.Field()
    delete_validity_ranges = ValidityRangeBatchDeleteMutation.Field()
    update_validity_ranges = ValidityRangeBatchPatchMutation.Field()
    publish_validity_range = PublishValidityRangeMutation.Field()

    create_time_grids = TimeGridBatchCreateMutation.Field()
    delete_time_grids = TimeGridBatchDeleteMutation.Field()
    update_time_grids = TimeGridBatchDeleteMutation.Field()

    create_lesson_bundles = LessonBundleBatchCreateMutation.Field()
    delete_lesson_bundles = LessonBundleBatchDeleteMutation.Field()
    update_lesson_bundles = LessonBundleBatchPatchMutation.Field()

    update_lessons = LessonBatchPatchMutation.Field()

    create_supervisions = SupervisionBatchCreateMutation.Field()
    delete_supervisions = SupervisionBatchDeleteMutation.Field()
    update_supervisions = SupervisionBatchPatchMutation.Field()

    create_courses_for_validity_range = CourseBatchCreateForValidityRangeMutation.Field()
