<script setup>
import SubjectChip from "./SubjectChip.vue";
</script>

<template>
  <v-autocomplete
    v-bind="$attrs"
    v-on="$listeners"
    multiple
    :items="teacherList"
    item-text="fullName"
    item-value="id"
    :loading="loading"
    :disabled="loading"
    @click="fetchCalendar"
  >
    <template #item="data">
      <v-list-item-action>
        <v-checkbox v-model="data.attrs.inputValue" />
      </v-list-item-action>
      <v-list-item-content>
        <v-list-item-title>
          {{ data.item.fullName }}
          <span v-if="data.item.shortName" class="text--secondary">
            {{ ` · ${data.item.shortName}` }}
          </span>
        </v-list-item-title>
        <v-list-item-subtitle
          v-if="
            (showSubjects && data.item.subjectsAsTeacher.length) ||
            availabilityCheckReady
          "
          class="d-flex align-center"
        >
          <subject-chip
            v-for="(subject, i) in data.item.subjectsAsTeacher"
            :key="subject.id"
            :subject="subject"
            :short-name="true"
            x-small
            outlined
            :class="{
              'text--secondary': subject.id !== prioritySubject.id,
              'mr-1': i < data.item.subjectsAsTeacher.length - 1,
            }"
            :style="{ 'vertical-align': 'middle' }"
          />
          <span
            v-if="
              showSubjects &&
              data.item.subjectsAsTeacher.length &&
              availabilityCheckReady
            "
            class="mx-1"
          >
            ·
          </span>
          <span v-if="availabilityCheckReady">{{
            data.item.available
              ? $t("cursus.teachers.field.availability.available")
              : $t("cursus.teachers.field.availability.unavailable")
          }}</span>
        </v-list-item-subtitle>
      </v-list-item-content>

      <v-list-item-action
        v-if="(prioritySubject || availabilityCheckReady) && showStatusChip"
      >
        <v-chip :color="getStatusColor(data.item)" outlined small class="mr-1">
          <v-icon small left>
            {{ getStatusIcon(data.item) }}
          </v-icon>
          {{ getStatusText(data.item) }}
        </v-chip>
      </v-list-item-action>
    </template>
    <template #prepend-inner>
      <slot name="prepend-inner" />
    </template>
    <template #selection="data">
      <slot name="selection" v-bind="data">
        <v-chip small>
          {{ data.item.shortName ? data.item.shortName : data.item.fullName }}
        </v-chip>
      </slot>
    </template>
  </v-autocomplete>
</template>

<script>
import { gqlCalendar, gqlTeachers } from "./helper.graphql";

export default {
  name: "TeacherField",
  data() {
    return {
      persons: [],
      calendar: {
        calendarFeeds: [],
      },
    };
  },
  props: {
    showSubjects: {
      type: Boolean,
      required: false,
      default: false,
    },
    prioritySubject: {
      type: Object,
      required: false,
      default: null,
    },
    availabilityDatetimeStart: {
      type: String,
      required: false,
      default: null,
    },
    availabilityDatetimeEnd: {
      type: String,
      required: false,
      default: null,
    },
    showStatusChip: {
      type: Boolean,
      required: false,
      default: true,
    },
    customTeachers: {
      type: Array,
      required: false,
      default: () => [],
    },
  },
  computed: {
    innerTeachers() {
      if (this.customTeachers.length > 0) {
        return this.customTeachers;
      } else {
        return this.persons;
      }
    },
    teacherList() {
      let sortedTeachers = this.innerTeachers;

      if (this.prioritySubject) {
        let matching = [];
        let nonMatching = [];

        sortedTeachers.forEach((p) => {
          if (
            p.subjectsAsTeacher.some((s) => s.id === this.prioritySubject.id)
          ) {
            matching.push({ ...p, hasSubject: true });
          } else {
            nonMatching.push({ ...p, hasSubject: false });
          }
        });

        sortedTeachers = matching.concat(nonMatching);
      }
      if (this.availabilityCheckReady) {
        let available = [];
        let unavailable = [];

        sortedTeachers.forEach((p) => {
          if (this.unavailableTeachers.some((t) => t == p.id)) {
            unavailable.push({ ...p, available: false });
          } else {
            available.push({ ...p, available: true });
          }
        });

        sortedTeachers = available.concat(unavailable);
      }

      return sortedTeachers;
    },
    loading() {
      return (
        this.$apollo.queries.calendar.loading ||
        this.$apollo.queries.persons.loading
      );
    },
    availabilityCheckEnabled() {
      return !!(this.availabilityDatetimeStart && this.availabilityDatetimeEnd);
    },
    availabilityCheckQueryReady() {
      return this.availabilityCheckEnabled && this.innerTeachers.length;
    },
    availabilityCheckReady() {
      return !!(
        this.availabilityCheckEnabled &&
        this.availabilityEvents?.length &&
        this.unavailableTeachers?.length
      );
    },
    availabilityEvents() {
      return this.calendar.calendarFeeds[0]?.events;
    },
    unavailableTeachers() {
      return this.availabilityEvents
        ?.map((e) => JSON.parse(e.meta)?.persons)
        .flat();
    },
    calendarQueryVariables() {
      return {
        datetimeStart: this.availabilityDatetimeStart,
        datetimeEnd: this.availabilityDatetimeEnd,
        names: ["free_busy"],
        params: JSON.stringify({
          persons: this.innerTeachers.map((p) => p.id),
        }),
      };
    },
  },
  methods: {
    getStatusColor(item) {
      if (!Object.hasOwn(item, "available") || item.available) {
        if (!Object.hasOwn(item, "hasSubject") || item.hasSubject) {
          return "success";
        } else {
          return "warning";
        }
      } else {
        return "error";
      }
    },
    getStatusIcon(item) {
      if (!Object.hasOwn(item, "available") || item.available) {
        if (!Object.hasOwn(item, "hasSubject") || item.hasSubject) {
          return "$success";
        } else {
          return "$warning";
        }
      } else {
        return "$error";
      }
    },
    getStatusText(item) {
      if (!Object.hasOwn(item, "available") || item.available) {
        if (!Object.hasOwn(item, "hasSubject") || item.hasSubject) {
          return this.$t("cursus.teachers.field.status.good_fit");
        } else {
          return this.$t("cursus.teachers.field.status.misses_subject");
        }
      } else {
        return this.$t("cursus.teachers.field.availability.unavailable");
      }
    },
    fetchCalendar() {
      if (this.availabilityCheckQueryReady) {
        this.$apollo.queries.calendar.skip = false;
        this.$apollo.queries.calendar.refetch();
      }
    },
  },
  apollo: {
    persons: {
      query: gqlTeachers,
      skip() {
        return this.customTeachers.length > 0;
      },
    },
    calendar: {
      query: gqlCalendar,
      skip: true,
      variables() {
        return this.calendarQueryVariables;
      },
    },
  },
};
</script>

<style scoped></style>
