from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import graphene
from graphene_django.types import DjangoObjectType
from graphene_django_cud.mutations import (
    DjangoBatchCreateMutation,
    DjangoBatchDeleteMutation,
    DjangoBatchPatchMutation,
)

from aleksis.apps.cursus.models import Course, Subject
from aleksis.apps.cursus.schema import CourseType, SubjectType
from aleksis.core.models import Group, Person
from aleksis.core.schema.base import (
    DjangoFilterMixin,
    PermissionBatchPatchMixin,
    PermissionsTypeMixin,
)
from aleksis.core.util.core_helpers import (
    get_active_school_term,
    get_site_preferences,
)

from ..models import TimeboundCourseConfig, ValidityRange

timebound_course_config_filters = {"course": ["in"], "validity_range": ["in"], "teachers": [""]}


class TimeboundCourseConfigType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    class Meta:
        model = TimeboundCourseConfig
        fields = ("id", "course", "validity_range", "lesson_quota", "teachers")
        filter_fields = timebound_course_config_filters

    @staticmethod
    def resolve_name(root, info, **kwargs):
        return root.course.name

    @staticmethod
    def resolve_subject(root, info, **kwargs):
        return root.course.subject

    @staticmethod
    def resolve_groups(root, info, **kwargs):
        return root.course.groups.all()

    @staticmethod
    def resolve_lesson_quota(root, info, **kwargs):
        return root.lesson_quota

    @staticmethod
    def resolve_teachers(root, info, **kwargs):
        return root.teachers.all()

    @staticmethod
    def resolve_course_id(root, info, **kwargs):
        return root.course.id


class LesroosterExtendedCourseType(CourseType):
    class Meta:
        model = Course

    lr_timebound_course_configs = graphene.List(TimeboundCourseConfigType)

    @staticmethod
    def resolve_lr_timebound_course_configs(root, info, **kwargs):
        if info.context.user.has_perm("lesrooster.view_timeboundcourseconfig_rule"):
            return root.lr_timebound_course_configs.all()
        return []


class LesroosterExtendedSubjectType(SubjectType):
    class Meta:
        model = Subject

    courses = graphene.List(LesroosterExtendedCourseType)


class TimeboundCourseConfigBatchCreateMutation(DjangoBatchCreateMutation):
    class Meta:
        model = TimeboundCourseConfig
        fields = ("id", "course", "validity_range", "lesson_quota", "teachers")
        permissions = ("lesrooster.create_timeboundcourseconfig_rule",)


class TimeboundCourseConfigBatchDeleteMutation(DjangoBatchDeleteMutation):
    class Meta:
        model = TimeboundCourseConfig
        permission_required = "lesrooster.delete_timeboundcourseconfig_rule"


class TimeboundCourseConfigBatchPatchMutation(PermissionBatchPatchMixin, DjangoBatchPatchMutation):
    class Meta:
        model = TimeboundCourseConfig
        fields = ("id", "course", "validity_range", "lesson_quota", "teachers")
        permissions = ("lesrooster.change_timeboundcourseconfig_rule",)


class CourseInputType(graphene.InputObjectType):
    name = graphene.String(required=True)
    subject = graphene.ID(required=True)
    teachers = graphene.List(graphene.ID, required=True)
    groups = graphene.List(graphene.ID, required=True)

    lesson_quota = graphene.Int(required=False)
    default_room = graphene.ID(required=False)


class CourseBatchCreateForValidityRangeMutation(graphene.Mutation):
    class Arguments:
        input = graphene.List(CourseInputType)
        validity_range = graphene.ID()

    courses = graphene.List(LesroosterExtendedCourseType)

    @classmethod
    def create(cls, info, course_input, validity_range):
        if info.context.user.has_perm("cursus.create_course_rule"):
            groups = Group.objects.filter(pk__in=course_input.groups)
            subject = Subject.objects.get(pk=course_input.subject)
            teachers = Person.objects.filter(pk__in=course_input.teachers)
            validity_range = ValidityRange.objects.get(pk=validity_range)

            course = Course.objects.create(
                name=f"""{''.join(groups.values_list('short_name', flat=True)
                .order_by('short_name'))}-{subject.name}""",
                subject=subject,
                lesson_quota=course_input.lesson_quota or None,
            )
            course.teachers.set(teachers)

            tcc = TimeboundCourseConfig.objects.create(
                course=course,
                validity_range=validity_range,
                lesson_quota=course.lesson_quota,
            )
            tcc.teachers.set(course.teachers.all())

            if get_site_preferences()["lesrooster__create_course_group"]:
                school_term = get_active_school_term(info.context)

                if school_term is None:
                    raise ValidationError(_("There is no school term for the school structure."))

                group_type = get_site_preferences()["lesrooster__group_type_course_groups"]

                course_group, created = Group.objects.get_or_create(
                    school_term=school_term,
                    group_type=group_type,
                    short_name=f"""{''.join(groups.values_list('short_name', flat=True)
                                      .order_by('short_name'))}-{subject.short_name}""",
                    name=f"""{', '.join(groups.values_list('short_name', flat=True)
                                      .order_by('short_name'))}-{subject.name}""",
                )
                if get_site_preferences()["lesrooster__fill_course_groups_with_members"]:
                    members = Person.objects.filter(pk__in=groups.values_list("members", flat=True))
                    course_group.members.set(members)
                course_group.owners.set(teachers)
                course_group.parent_groups.set(groups)
                course_group.save()
                course.groups.set([course_group])
            else:
                course.groups.set(groups)

            course.save()
            return course

    @classmethod
    def mutate(cls, root, info, input, validity_range):  # noqa
        objs = [cls.create(info, course_input, validity_range) for course_input in input]
        return CourseBatchCreateForValidityRangeMutation(courses=objs)
