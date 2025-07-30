<template>
  <dialog-object-form v-bind="$props" v-on="$listeners">
    <template #activator="{ on, attrs }">
      <slot name="activator" v-bind="{ on, attrs }" />
    </template>

    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #name.field="{ attrs, on }">
      <div aria-required="true">
        <v-text-field v-bind="attrs" v-on="on" :rules="rules.name" />
      </div>
    </template>

    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #lessonQuota.field="{ attrs, on }">
      <positive-small-integer-field v-bind="attrs" v-on="on" />
    </template>

    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #courses.field="{ attrs, on }">
      <div aria-required="true">
        <v-autocomplete
          multiple
          :items="courses"
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
  </dialog-object-form>
</template>

<script>
import DialogObjectForm from "aleksis.core/components/generic/dialogs/DialogObjectForm.vue";
import PositiveSmallIntegerField from "aleksis.core/components/generic/forms/PositiveSmallIntegerField.vue";

export default {
  name: "CreateCourseBundle",
  extends: DialogObjectForm,
  components: {
    DialogObjectForm,
    PositiveSmallIntegerField,
  },
  props: {
    courses: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
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
};
</script>
