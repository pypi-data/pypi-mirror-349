<script setup>
import InlineCRUDList from "aleksis.core/components/generic/InlineCRUDList.vue";
import PositiveSmallIntegerField from "aleksis.core/components/generic/forms/PositiveSmallIntegerField.vue";
import SubjectChip from "./SubjectChip.vue";
import CreateButton from "aleksis.core/components/generic/buttons/CreateButton.vue";
// eslint-disable-next-line no-unused-vars
import CreateCourse from "./CreateCourse.vue";
import CreateCourseBundle from "./CreateCourseBundle.vue";
import SubjectField from "./SubjectField.vue";
</script>

<template>
  <inline-c-r-u-d-list
    :headers="headers"
    :i18n-key="i18nKey"
    create-item-i18n-key="cursus.course.create"
    :gql-query="gqlQuery"
    :gql-create-mutation="gqlCreateMutation"
    :gql-patch-mutation="gqlPatchMutation"
    :gql-delete-mutation="gqlDeleteMutation"
    :default-item="defaultItem"
    :actions="[makeCourseBundleAction]"
    @items="allCourses = $event"
  >
    <template #createComponent="{ attrs, on, createMode }">
      <create-button
        color="secondary"
        @click="on.input(true)"
        :disabled="createMode"
      />

      <create-course v-bind="attrs" v-on="on" :gql-query="gqlQuery" />
    </template>

    <template #additionalActions>
      <create-course-bundle
        v-model="createCourseBundleMode"
        :fields="courseBundleFields"
        :default-item="defaultCourseBundle"
        force-model-item-update
        create-item-i18n-key="cursus.course_bundle.create"
        :gql-create-mutation="gqlCreateCourseBundles"
        :get-create-data="transformCreateCourseBundlesData"
        :courses="allCourses"
      />
    </template>

    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #name.field="{ attrs, on }">
      <div aria-required="true">
        <v-text-field v-bind="attrs" v-on="on" required :rules="rules.name" />
      </div>
    </template>

    <template #subject="{ item }">
      <subject-chip v-if="item.subject" :subject="item.subject" />
    </template>
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #subject.field="{ attrs, on }">
      <div aria-required="true">
        <subject-field
          v-bind="attrs"
          v-on="on"
          :rules="rules.subject"
          required
          :return-object="false"
        />
      </div>
    </template>

    <template #teachers="{ item }">
      <v-chip v-for="teacher in item.teachers" :key="teacher.id">{{
        teacher.fullName
      }}</v-chip
      >&nbsp;
    </template>
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #teachers.field="{ attrs, on }">
      <div aria-required="true">
        <v-autocomplete
          multiple
          :items="persons"
          item-text="fullName"
          item-value="id"
          v-bind="attrs"
          v-on="on"
          chips
          deletable-chips
          required
          :rules="rules.requiredList"
        >
          <template #item="data">
            <v-list-item-action>
              <v-checkbox v-model="data.attrs.inputValue" />
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>{{ data.item.fullName }}</v-list-item-title>
              <v-list-item-subtitle v-if="data.item.shortName">{{
                data.item.shortName
              }}</v-list-item-subtitle>
            </v-list-item-content>
          </template>
        </v-autocomplete>
      </div>
    </template>

    <template #groups="{ item }">
      <v-chip v-for="group in item.groups" :key="group.id">{{
        group.name
      }}</v-chip
      >&nbsp;
    </template>
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #groups.field="{ attrs, on }">
      <div aria-required="true">
        <v-autocomplete
          multiple
          :items="groups"
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

    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #lessonQuota.field="{ attrs, on }">
      <positive-small-integer-field v-bind="attrs" v-on="on" />
    </template>
  </inline-c-r-u-d-list>
</template>

<script>
import courseBundleFieldsMixin from "./courseBundleFieldsMixin.js";

import {
  courses,
  createCourses,
  deleteCourses,
  updateCourses,
} from "./course.graphql";

import { createCourseBundles } from "./courseBundle.graphql";

import { gqlGroups, gqlPersons } from "./helper.graphql";

export default {
  name: "Course",
  mixins: [courseBundleFieldsMixin],
  data() {
    return {
      headers: [
        {
          text: this.$t("cursus.course.fields.name"),
          value: "name",
        },
        {
          text: this.$t("cursus.course.fields.subject"),
          value: "subject",
          orderKey: "subject__name",
        },
        {
          text: this.$t("cursus.course.fields.groups"),
          value: "groups",
        },
        {
          text: this.$t("cursus.course.fields.teachers"),
          value: "teachers",
        },
        {
          text: this.$t("cursus.course.fields.lesson_quota"),
          value: "lessonQuota",
        },
      ],
      i18nKey: "cursus.course",
      gqlQuery: courses,
      gqlCreateMutation: createCourses,
      gqlPatchMutation: updateCourses,
      gqlDeleteMutation: deleteCourses,
      defaultItem: {
        name: "",
        subject: null,
        teachers: [],
        groups: [],
        lessonQuota: null,
      },
      rules: {
        name: [
          (name) =>
            (name && name.length > 0) || this.$t("cursus.errors.name_required"),
        ],
        subject: [
          (subject) => !!subject || this.$t("cursus.errors.subject_required"),
        ],
        requiredList: [
          (list) =>
            (!!list && list.length > 0) || this.$t("forms.errors.required"),
        ],
      },
      gqlCreateCourseBundles: createCourseBundles,
      groups: [],
      allCourses: [],
      defaultCourseBundle: { courses: [] },
      createCourseBundleMode: false,
      makeCourseBundleAction: {
        name: this.$t("cursus.course_bundle.create"),
        icon: "$edit",
        predicate: (item) => true,
        handler: (items) => {
          this.$set(this.defaultCourseBundle, "courses", items);
          this.createCourseBundleMode = true;
        },
        clearSelection: true,
      },
    };
  },
  methods: {
    transformCreateCourseBundlesData(courseBundle) {
      return {
        ...courseBundle,
        courses: courseBundle.courses.map((course) => course.id),
      };
    },
  },
  apollo: {
    persons: gqlPersons,
    groups: gqlGroups,
  },
};
</script>
