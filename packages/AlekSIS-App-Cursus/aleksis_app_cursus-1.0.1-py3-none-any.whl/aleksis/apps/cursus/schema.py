from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

import graphene
import graphene_django_optimizer
from graphene_django.types import DjangoObjectType
from graphene_django_cud.mutations import (
    DjangoBatchCreateMutation,
    DjangoBatchDeleteMutation,
    DjangoBatchPatchMutation,
)
from guardian.shortcuts import get_objects_for_user

from aleksis.core.models import Group, Person
from aleksis.core.schema.base import (
    DjangoFilterMixin,
    FilterOrderList,
    PermissionBatchDeleteMixin,
    PermissionBatchPatchMixin,
    PermissionsTypeMixin,
)
from aleksis.core.schema.group import GroupType as GraphQLGroupType
from aleksis.core.schema.group_type import GroupTypeType
from aleksis.core.schema.person import PersonType as GraphQLPersonType
from aleksis.core.util.core_helpers import (
    filter_active_school_term,
    get_active_school_term,
    get_site_preferences,
    has_person,
)

from .models import Course, CourseBundle, Subject


class SubjectType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    class Meta:
        model = Subject
        fields = (
            "id",
            "short_name",
            "name",
            "parent",
            "colour_fg",
            "colour_bg",
            "courses",
            "teachers",
        )
        filter_fields = {
            "id": ["exact"],
            "short_name": ["exact", "icontains"],
            "name": ["exact", "icontains"],
            "parent": ["exact", "in"],
            "colour_fg": ["exact"],
            "colour_bg": ["exact"],
            "courses": ["exact", "in"],
            "teachers": ["exact", "in"],
        }

    @staticmethod
    def resolve_courses(root, info, **kwargs):
        return get_objects_for_user(info.context.user, "cursus.view_course", root.courses.all())

    @staticmethod
    def resolve_teachers(root, info, **kwargs):
        if not info.context.user.has_perm("cursus.view_subject_details_rule", root):
            return []
        return graphene_django_optimizer.query(root.teachers.all(), info)


class SubjectBatchCreateMutation(DjangoBatchCreateMutation):
    class Meta:
        model = Subject
        permissions = ("cursus.create_subject_rule",)
        only_fields = (
            "short_name",
            "name",
            "parent",
            "colour_fg",
            "colour_bg",
            "courses",
            "teachers",
        )


class SubjectBatchDeleteMutation(PermissionBatchDeleteMixin, DjangoBatchDeleteMutation):
    class Meta:
        model = Subject
        permissions = ("cursus.delete_subject_rule",)


class SubjectBatchPatchMutation(PermissionBatchPatchMixin, DjangoBatchPatchMutation):
    class Meta:
        model = Subject
        permissions = ("cursus.edit_subject_rule",)
        only_fields = (
            "id",
            "short_name",
            "name",
            "parent",
            "colour_fg",
            "colour_bg",
            "courses",
            "teachers",
        )


class BaseCourseType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    """The abstract CourseType. It can be reused elsewhere."""

    class Meta:
        abstract = True

    @staticmethod
    def resolve_teachers(root, info, **kwargs):
        if not info.context.user.has_perm("cursus.view_course_details_rule", root):
            raise PermissionDenied()
        teachers = get_objects_for_user(info.context.user, "core.view_person", root.teachers.all())

        # Fixme: this following code was copied from aleksis/core/schema/group.py so it should work
        #        It does however fail with the message "'Person' object has no attribute 'query'"
        # if has_person(info.context.user) and [
        #     m for m in root.teachers.all() if m.pk == info.context.user.person.pk
        # ]:
        #     teachers = (teachers | Person.objects.get(pk=info.context.user.person.pk)).distinct()
        return graphene_django_optimizer.query(teachers, info)

    @staticmethod
    def resolve_groups(root, info, **kwargs):
        if not info.context.user.has_perm("cursus.view_course_details_rule", root):
            raise PermissionDenied()
        by_permission = get_objects_for_user(
            info.context.user, "core.view_group", root.groups.all()
        )
        by_ownership = info.context.user.person.owner_of.all() & root.groups.all()
        return graphene_django_optimizer.query(by_permission | by_ownership, info)

    @staticmethod
    def resolve_course_id(root, info, **kwargs):
        return root.id


class CourseType(BaseCourseType):
    """The concrete CourseType"""

    class Meta:
        model = Course
        fields = ("id", "name", "subject", "teachers", "groups", "lesson_quota", "default_room")
        filter_fields = {
            "id": ["exact"],
            "name": ["exact", "icontains"],
            "subject": ["exact", "in"],
            "subject__name": ["icontains"],
            "subject__short_name": ["icontains"],
            "teachers": ["in"],
            "groups": ["in"],
        }


class TeacherType(GraphQLPersonType):
    class Meta:
        model = Person

    subjects_as_teacher = graphene.List(SubjectType)
    courses_as_teacher = graphene.List(CourseType)

    @staticmethod
    def resolve_subjects_as_teacher(root, info, **kwargs):
        return graphene_django_optimizer.query(root.subjects_as_teacher.all(), info)

    @staticmethod
    def resolve_courses_as_teacher(root, info, **kwargs):
        return graphene_django_optimizer.query(root.courses_as_teacher.all(), info)


class CourseBatchCreateMutation(DjangoBatchCreateMutation):
    class Meta:
        model = Course
        permissions = ("cursus.create_course_rule",)
        only_fields = ("name", "subject", "teachers", "groups", "lesson_quota")


class CourseBatchDeleteMutation(PermissionBatchDeleteMixin, DjangoBatchDeleteMutation):
    class Meta:
        model = Course
        permissions = ("cursus.delete_course_rule",)


class CourseBatchPatchMutation(PermissionBatchPatchMixin, DjangoBatchPatchMutation):
    class Meta:
        model = Course
        permissions = ("cursus.edit_course_rule",)
        only_fields = ("id", "name", "subject", "teachers", "groups", "lesson_quota")


class BaseCourseBundleType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    """The abstract CourseBundleType. It can be reused elsewhere."""

    class Meta:
        abstract = True


class CourseBundleType(BaseCourseBundleType):
    """The concrete CourseBundleType"""

    class Meta:
        model = CourseBundle
        fields = ("id", "name", "courses", "lesson_quota")
        filter_fields = {
            "id": ["exact"],
            "name": ["exact", "icontains"],
            "groups": ["in"],
            "courses": ["in"],
        }


class CourseBundleBatchCreateMutation(DjangoBatchCreateMutation):
    class Meta:
        model = CourseBundle
        permissions = ("cursus.create_course_bundle_rule",)
        only_fields = ("name", "courses", "lesson_quota")


class CourseBundleBatchDeleteMutation(PermissionBatchDeleteMixin, DjangoBatchDeleteMutation):
    class Meta:
        model = CourseBundle
        permissions = ("cursus.delete_course_bundle_rule",)


class CourseBundleBatchPatchMutation(PermissionBatchPatchMixin, DjangoBatchPatchMutation):
    class Meta:
        model = CourseBundle
        permissions = ("cursus.edit_course_bundle_rule",)
        only_fields = ("id", "name", "courses", "lesson_quota")


class CreateSchoolStructureSecondLevelGroupsMutation(DjangoBatchCreateMutation):
    class Meta:
        model = Group
        permissions = ("core.add_group",)
        only_fields = ("name", "short_name", "parent_groups")

    @classmethod
    def before_mutate(cls, root, info, input):  # noqa
        group_type = get_site_preferences()["cursus__school_structure_second_level_group_type"]
        if not group_type:
            raise PermissionDenied()

        active_school_term = get_active_school_term(info.context)

        if active_school_term is None:
            raise ValidationError(_("There is no school term for the school structure."))

        for group in input:
            group["group_type"] = group_type.pk
            group["school_term"] = active_school_term.pk

        return input


class CreateSchoolStructureFirstLevelGroupsMutation(DjangoBatchCreateMutation):
    class Meta:
        model = Group
        permissions = ("core.add_group",)
        only_fields = ("name", "short_name", "parent_groups")

    @classmethod
    def before_mutate(cls, root, info, input):  # noqa
        group_type = get_site_preferences()["cursus__school_structure_first_level_group_type"]
        if not group_type:
            raise PermissionDenied()

        active_school_term = get_active_school_term(info.context)

        if active_school_term is None:
            raise ValidationError(_("There is no school term for the school structure."))

        for group in input:
            group["group_type"] = group_type.pk
            group["school_term"] = active_school_term.pk

        return input


class SchoolStructureQuery(graphene.ObjectType):
    first_level_type = graphene.Field(GroupTypeType)
    second_level_type = graphene.Field(GroupTypeType)
    first_level_groups = FilterOrderList(GraphQLGroupType)
    second_level_groups = FilterOrderList(GraphQLGroupType)

    @staticmethod
    def resolve_first_level_type(root, info, **kwargs):
        return get_site_preferences()["cursus__school_structure_first_level_group_type"]

    @staticmethod
    def resolve_second_level_type(root, info, **kwargs):
        return get_site_preferences()["cursus__school_structure_second_level_group_type"]

    @staticmethod
    def resolve_second_level_groups(root, info, **kwargs):
        group_type = get_site_preferences()["cursus__school_structure_second_level_group_type"]
        if not group_type:
            return []
        school_term = get_active_school_term(info.context)
        qs = get_objects_for_user(
            info.context.user,
            "core.view_group",
            Group.objects.filter(school_term=school_term, group_type=group_type),
        )
        return graphene_django_optimizer.query(qs, info)

    @staticmethod
    def resolve_first_level_groups(root, info):
        group_type = get_site_preferences()["cursus__school_structure_first_level_group_type"]
        if not group_type:
            return []
        school_term = get_active_school_term(info.context)
        qs = get_objects_for_user(
            info.context.user,
            "core.view_group",
            Group.objects.filter(school_term=school_term, group_type=group_type),
        )
        return graphene_django_optimizer.query(qs, info)


class Query(graphene.ObjectType):
    subjects = FilterOrderList(SubjectType)
    courses = FilterOrderList(CourseType)
    course_bundles = FilterOrderList(CourseBundleType)

    school_structure = graphene.Field(SchoolStructureQuery)

    teachers = FilterOrderList(TeacherType)

    course_by_id = graphene.Field(CourseType, id=graphene.ID())
    courses_of_teacher = FilterOrderList(CourseType, teacher=graphene.ID())

    @staticmethod
    def resolve_subjects(root, info, **kwargs):
        if not info.context.user.has_perm("cursus.view_subject_rule"):
            return []
        return graphene_django_optimizer.query(Subject.objects.all(), info)

    @staticmethod
    def resolve_courses(root, info, **kwargs):
        qs = filter_active_school_term(
            info.context, Course.objects.all(), school_term_field="groups__school_term"
        )
        return graphene_django_optimizer.query(qs, info)

    @staticmethod
    def resolve_course_by_id(root, info, id):  # noqa
        course = Course.objects.get(pk=id)
        if not info.context.user.has_perm("cursus.view_course_rule", course):
            raise PermissionDenied()
        return course

    @staticmethod
    def resolve_teachers(root, info):
        qs = get_objects_for_user(
            info.context.user,
            "core.view_person",
            Person.objects.filter(
                Q(courses_as_teacher__isnull=False) | Q(subjects_as_teacher__isnull=False)
            ).distinct(),
        )
        return graphene_django_optimizer.query(qs, info)

    @staticmethod
    def resolve_courses_of_teacher(root, info, teacher=None):
        if not has_person(info.context.user):
            raise PermissionDenied()
        teacher = Person.objects.get(pk=teacher) if teacher else info.context.user.person
        # FIXME: Permission checking. But maybe it's done in get_queryset
        qs = teacher.courses_as_teacher.all()
        return graphene_django_optimizer.query(qs, info)

    @staticmethod
    def resolve_school_structure(root, info):
        return True


class Mutation(graphene.ObjectType):
    create_subjects = SubjectBatchCreateMutation.Field()
    delete_subjects = SubjectBatchDeleteMutation.Field()
    update_subjects = SubjectBatchPatchMutation.Field()

    create_courses = CourseBatchCreateMutation.Field()
    delete_courses = CourseBatchDeleteMutation.Field()
    update_courses = CourseBatchPatchMutation.Field()

    create_course_bundles = CourseBundleBatchCreateMutation.Field()
    delete_course_bundles = CourseBundleBatchDeleteMutation.Field()
    update_course_bundles = CourseBundleBatchPatchMutation.Field()

    create_first_level_groups = CreateSchoolStructureFirstLevelGroupsMutation.Field()
    create_second_level_groups = CreateSchoolStructureSecondLevelGroupsMutation.Field()
