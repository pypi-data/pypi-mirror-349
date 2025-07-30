<template>
  <inline-c-r-u-d-list
    :headers="courseBundleFields"
    :i18n-key="i18nKey"
    create-item-i18n-key="cursus.course_bundle.create"
    :gql-query="gqlQuery"
    :gql-create-mutation="gqlCreateMutation"
    :default-item="defaultItem"
    :gql-patch-mutation="gqlPatchMutation"
    :gql-delete-mutation="gqlDeleteMutation"
  >
    <template #createComponent="{ attrs, on, createMode }">
      <create-button
        color="secondary"
        @click="on.input(true)"
        :disabled="createMode"
      />
      <create-course-bundle v-bind="attrs" v-on="on" :courses="items" />
    </template>

    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #name.field="{ attrs, on }">
      <div aria-required="true">
        <v-text-field v-bind="attrs" v-on="on" required :rules="rules.name" />
      </div>
    </template>

    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #lessonQuota.field="{ attrs, on }">
      <positive-small-integer-field v-bind="attrs" v-on="on" />
    </template>

    <template #courses="{ item }">
      <v-chip v-for="course in item.courses" :key="course.id">{{
        course.name
      }}</v-chip
      >&nbsp;
    </template>
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #courses.field="{ attrs, on }">
      <div aria-required="true">
        <v-autocomplete
          multiple
          :items="items"
          item-text="name"
          item-value="id"
          v-bind="attrs"
          v-on="on"
          chips
          deletable-chips
          required
          :rules="rules.requiredList"
        />
      </div>
    </template>
  </inline-c-r-u-d-list>
</template>

<script>
import InlineCRUDList from "aleksis.core/components/generic/InlineCRUDList.vue";
import PositiveSmallIntegerField from "aleksis.core/components/generic/forms/PositiveSmallIntegerField.vue";
import CreateButton from "aleksis.core/components/generic/buttons/CreateButton.vue";
import CreateCourseBundle from "./CreateCourseBundle.vue";

import courseBundleFieldsMixin from "./courseBundleFieldsMixin.js";

import {
  courseBundles,
  createCourseBundles,
  deleteCourseBundles,
  updateCourseBundles,
} from "./courseBundle.graphql";

import { courses } from "./course.graphql";

export default {
  name: "CourseBundle",
  components: {
    InlineCRUDList,
    PositiveSmallIntegerField,
    CreateButton,
    CreateCourseBundle,
  },
  mixins: [courseBundleFieldsMixin],
  data() {
    return {
      i18nKey: "cursus.course_bundle",
      gqlQuery: courseBundles,
      gqlCreateMutation: createCourseBundles,
      gqlPatchMutation: updateCourseBundles,
      gqlDeleteMutation: deleteCourseBundles,
      defaultItem: {
        name: "",
        lessonQuota: null,
        courses: [],
      },
      rules: {
        name: [
          (name) =>
            (name && name.length > 0) || this.$t("cursus.errors.name_required"),
        ],
        requiredList: [
          (list) =>
            (!!list && list.length > 0) || this.$t("forms.errors.required"),
        ],
      },
    };
  },
  apollo: {
    items: courses,
  },
};
</script>
