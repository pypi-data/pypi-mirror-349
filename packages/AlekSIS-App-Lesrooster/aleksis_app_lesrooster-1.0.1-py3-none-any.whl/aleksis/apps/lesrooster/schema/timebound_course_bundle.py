import graphene

from aleksis.apps.cursus.models import Course, CourseBundle
from aleksis.apps.cursus.schema import BaseCourseBundleType, BaseCourseType

from ..models import TimeboundCourseConfig


class TimeboundCourseType(BaseCourseType):
    class Meta:
        # Do not register as type for model. Use only if explicit request.
        skip_registry = True
        model = Course
        fields = ("id", "name", "subject", "teachers", "groups", "lesson_quota", "default_room")

    def resolve_lesson_quota(root, info):
        """Resolve lesson_quota from timebound_course_config"""
        return TimeboundCourseConfig.objects.get(
            course=root,
            validity_range__id=root.validity_range_id,
        ).lesson_quota

    def resolve_teachers(root, info):
        """Resolve teachers from timebound_course_config"""
        return TimeboundCourseConfig.objects.get(
            course=root, validity_range__id=root.validity_range_id
        ).teachers.all()


class TimeboundCourseBundleType(BaseCourseBundleType):
    class Meta:
        # Do not register as type for model. Use only if explicit request.
        skip_registry = True
        model = CourseBundle
        fields = ("id", "name", "lesson_quota")

    courses = graphene.List(TimeboundCourseType)

    def resolve_courses(root, info):
        courses = root.courses.all()
        for course in courses:
            course.validity_range_id = root.validity_range_id

        return courses
