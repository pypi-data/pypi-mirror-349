from django.contrib.auth.models import User

from rules import predicate

from ..models import Course, CourseBundle


@predicate
def is_course_teacher(user: User, obj: Course) -> bool:
    """Check if person of user is teacher in a specific course."""
    return user.person in obj.teachers.all()


@predicate
def is_course_bundle_teacher(user: User, obj: CourseBundle) -> bool:
    """Check if person of user is teacher in a course of a specific course bundle."""
    return any([user.person in course.teachers.all() for course in obj.courses.all()])
