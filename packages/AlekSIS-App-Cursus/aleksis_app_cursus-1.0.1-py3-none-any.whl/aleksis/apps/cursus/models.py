from django.db import models
from django.utils.translation import gettext as _

from colorfield.fields import ColorField

from aleksis.core.mixins import ExtensibleModel, GlobalPermissionModel


class Subject(ExtensibleModel):
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, verbose_name=_("Parent subject"), blank=True, null=True
    )

    short_name = models.CharField(verbose_name=_("Short name"), max_length=255, unique=True)
    name = models.CharField(verbose_name=_("Long name"), max_length=255)

    colour_fg = ColorField(verbose_name=_("Foreground colour"), blank=True)
    colour_bg = ColorField(verbose_name=_("Background colour"), blank=True)

    teachers = models.ManyToManyField(
        "core.Person", related_name="subjects_as_teacher", verbose_name=_("Teachers")
    )

    class Meta:
        ordering = ["name", "short_name"]
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")

    def __str__(self) -> str:
        return f"{self.short_name} ({self.name})"

    def get_colour_fg(self):
        if not self.colour_fg and self.parent:
            return self.parent.colour_fg
        return self.colour_fg

    def get_colour_bg(self):
        if not self.colour_bg and self.parent:
            return self.parent.colour_bg
        return self.colour_bg


class CourseBundle(ExtensibleModel):
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    courses = models.ManyToManyField(
        "Course", related_name="bundle", verbose_name=_("Bundled courses")
    )

    lesson_quota = models.PositiveSmallIntegerField(
        verbose_name=_("Lesson quota"), blank=True, null=True
    )

    @classmethod
    def create_for_course(cls, course: "Course") -> "CourseBundle":
        bundle = cls.objects.create(
            managed_by_app_label=CourseBundle._meta.app_label,
            name=course.name,
            lesson_quota=course.lesson_quota,
        )
        bundle.courses.set([course])
        return bundle

    class Meta:
        ordering = ["name"]
        verbose_name = _("Course Bundle")
        verbose_name_plural = _("Course Bundles")

    def __str__(self):
        return self.name


class Course(ExtensibleModel):
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    subject = models.ForeignKey(
        "Subject",
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name=_("Subject"),
    )
    teachers = models.ManyToManyField(
        "core.Person", related_name="courses_as_teacher", verbose_name=_("Teachers")
    )
    groups = models.ManyToManyField("core.Group", related_name="courses", verbose_name=_("Groups"))

    lesson_quota = models.PositiveSmallIntegerField(
        verbose_name=_("Lesson quota"), blank=True, null=True
    )

    default_room = models.ForeignKey(
        "core.Room",
        on_delete=models.SET_NULL,
        related_name="courses",
        verbose_name=_("Default Room"),
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["subject"]
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if not self.name:
            group_names = [group.short_name or group.name for group in self.groups.all()]
            self.name = f"{group_names}-{self.subject.short_name or self.subject.name}"
        super().save(*args, **kwargs)

        if is_new:
            CourseBundle.create_for_course(self)


class CursusGlobalPermissions(GlobalPermissionModel):  # noqa: DJ10,DJ11,DJ08
    class Meta:
        managed = False
        permissions = (("manage_school_structure", _("Can manage school structure")),)
