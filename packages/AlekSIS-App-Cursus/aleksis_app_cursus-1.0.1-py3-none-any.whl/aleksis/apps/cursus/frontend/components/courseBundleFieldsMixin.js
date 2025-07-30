/**
 * Mixin providing the CourseBundle fields
 */
export default {
  data() {
    return {
      courseBundleFields: [
        {
          text: this.$t("cursus.course_bundle.fields.name"),
          value: "name",
        },
        {
          text: this.$t("cursus.course_bundle.fields.lesson_quota"),
          value: "lessonQuota",
        },
        {
          text: this.$t("cursus.course_bundle.fields.courses"),
          value: "courses",
          orderKey: "courses__name",
        },
      ],
    };
  },
};
