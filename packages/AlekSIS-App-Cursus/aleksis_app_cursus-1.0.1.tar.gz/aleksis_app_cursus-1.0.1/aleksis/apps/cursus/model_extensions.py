from django.apps import apps
from django.db.models import Model
from django.utils.translation import gettext as _

from .models import Course, CourseBundle, Subject

if apps.is_installed("aleksis.apps.csv_import"):
    from aleksis.apps.csv_import.field_types import ProcessFieldType

    class GroupSubjectByShortNameFieldType(ProcessFieldType):
        _class_name = "group_subject_short_name"
        verbose_name = _("Short name of the subject")

        def process(self, instance: Model, value):
            subject, __ = Subject.objects.get_or_create(short_name=value, defaults={"name": value})
            instance.subject = subject
            instance.save()

    class SubjectByShortNameFieldType(ProcessFieldType):
        _class_name = "subject_by_short_name"
        verbose_name = _("Short name of the subject")
        run_before_save = True

        def process(self, instance: Model, value):
            subject, __ = Subject.objects.get_or_create(short_name=value, defaults={"name": value})
            instance.subject = subject

    class CourseByUniqueReferenceFieldType(ProcessFieldType):
        _class_name = "course_by_unique_reference"
        verbose_name = _("Course by unique reference")
        run_before_save = True

        def process(self, instance: Model, value):
            course = Course.objects.get(extended_data__import_ref_csv=value)
            instance.course = course

    class CourseBundleByCourseUniqueReferenceFieldType(ProcessFieldType):
        _class_name = "course_bundle_by_course_unique_reference"
        verbose_name = _("Course bundle by course unique reference")
        run_before_save = True

        def process(self, instance: Model, value):
            course = Course.objects.get(extended_data__import_ref_csv=value)
            instance.course_bundle = course.bundle.first()

    class CourseBundleByCourse(ProcessFieldType):
        _class_name = "course_bundle_by_course"
        verbose_name = _("Create course bundle for this course")

        def process(self, instance: Course, value):
            if not instance.bundle.all():
                bundle = CourseBundle.objects.create(name=instance.name)
                bundle.courses.set([instance])
