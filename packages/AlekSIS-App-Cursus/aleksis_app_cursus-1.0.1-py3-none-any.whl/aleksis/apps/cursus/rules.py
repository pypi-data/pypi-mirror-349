from rules import add_perm

from aleksis.core.util.predicates import (
    has_any_object,
    has_global_perm,
    has_object_perm,
    has_person,
    is_site_preference_set,
)

from .models import Course, CourseBundle, Subject
from .util.predicates import is_course_bundle_teacher, is_course_teacher

view_subjects_predicate = has_person & (
    has_global_perm("cursus.view_subject") | has_any_object("cursus.view_subject", Subject)
)
add_perm("cursus.view_subjects_rule", view_subjects_predicate)

view_subject_predicate = has_person
add_perm("cursus.view_subject_rule", view_subject_predicate)

view_subject_details_predicate = view_subject_predicate & (
    has_global_perm("cursus.view_subject") | has_object_perm("cursus.view_subject")
)
add_perm("cursus.view_subject_details_rule", view_subject_details_predicate)

create_subject_predicate = has_person & has_global_perm("cursus.add_subject")
add_perm("cursus.create_subject_rule", create_subject_predicate)

edit_subject_predicate = view_subject_predicate & (
    has_global_perm("cursus.change_subject") | has_object_perm("cursus.change_subject")
)
add_perm("cursus.edit_subject_rule", edit_subject_predicate)

delete_subject_predicate = view_subject_predicate & (
    has_global_perm("cursus.delete_subject") | has_object_perm("cursus.delete_subject")
)
add_perm("cursus.delete_subject_rule", delete_subject_predicate)

view_courses_predicate = has_person & (
    has_global_perm("cursus.view_course") | has_any_object("cursus.view_course", Course)
)
add_perm("cursus.view_courses_rule", view_courses_predicate)

view_course_predicate = has_person
add_perm("cursus.view_course_rule", view_course_predicate)

view_course_details_predicate = has_person & (
    is_course_teacher
    | has_global_perm("cursus.view_course")
    | has_object_perm("cursus.view_course")
)
add_perm("cursus.view_course_details_rule", view_course_details_predicate)

create_course_predicate = has_person & has_global_perm("cursus.add_course")
add_perm("cursus.create_course_rule", create_course_predicate)

edit_course_predicate = view_course_predicate & (
    has_global_perm("cursus.change_course") | has_object_perm("cursus.change_course")
)
add_perm("cursus.edit_course_rule", edit_course_predicate)

delete_course_predicate = view_course_predicate & (
    has_global_perm("cursus.delete_course") | has_object_perm("cursus.delete_course")
)
add_perm("cursus.delete_course_rule", delete_course_predicate)

view_course_bundles_predicate = has_person & (
    has_global_perm("cursus.view_coursebundle")
    | has_any_object("cursus.view_coursebundle", CourseBundle)
)
add_perm("cursus.view_course_bundles_rule", view_course_bundles_predicate)

view_course_bundle_predicate = has_person
add_perm("cursus.view_course_bundle_rule", view_course_bundle_predicate)

view_course_bundle_details_predicate = has_person & (
    is_course_bundle_teacher
    | has_global_perm("cursus.view_coursebundle")
    | has_object_perm("cursus.view_coursebundle")
)
add_perm("cursus.view_course_bundle_details_rule", view_course_bundle_details_predicate)

create_course_bundle_predicate = has_person & has_global_perm("cursus.add_course_bundle")
add_perm("cursus.create_course_bundle_rule", create_course_bundle_predicate)

edit_course_bundle_predicate = view_course_bundle_predicate & (
    has_global_perm("cursus.change_course_bundle") | has_object_perm("cursus.change_course_bundle")
)
add_perm("cursus.edit_course_bundle_rule", edit_course_bundle_predicate)

delete_course_bundle_predicate = view_course_bundle_predicate & (
    has_global_perm("cursus.delete_course_bundle") | has_object_perm("cursus.delete_course_bundle")
)
add_perm("cursus.delete_course_bundle_rule", delete_course_bundle_predicate)

manage_school_structure_predicate = (
    has_person
    & is_site_preference_set("cursus", "school_structure_first_level_group_type")
    & is_site_preference_set("cursus", "school_structure_second_level_group_type")
    & has_global_perm("cursus.manage_school_structure")
)
add_perm("cursus.manage_school_structure_rule", manage_school_structure_predicate)

view_cursus_menu_predicate = (
    view_subjects_predicate | view_courses_predicate | manage_school_structure_predicate
)
add_perm("cursus.view_cursus_menu_rule", view_cursus_menu_predicate)
