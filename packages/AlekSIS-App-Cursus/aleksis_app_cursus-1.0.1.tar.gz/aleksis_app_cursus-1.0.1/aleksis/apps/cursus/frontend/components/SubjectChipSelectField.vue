<script setup>
import SubjectChip from "./SubjectChip.vue";
import ChipSelectField from "aleksis.core/components/generic/forms/ChipSelectField.vue";
</script>

<template>
  <chip-select-field
    v-bind="{ ...$props, ...$attrs }"
    v-on="$listeners"
    :background-color="$attrs?.value?.colourBg"
    :color="$attrs?.value?.colourFg"
    return-object
    item-text="name"
    item-value="id"
  >
    <template #item="{ item }">
      <subject-chip :subject="item" :style="{ cursor: 'pointer' }" />
    </template>
  </chip-select-field>
</template>

<script>
export default {
  name: "SubjectChipSelectField",
};
</script>

<style scoped></style>
