<script setup>
import ErrorPage from "aleksis.core/components/app/ErrorPage.vue";
import DialogObjectForm from "aleksis.core/components/generic/dialogs/DialogObjectForm.vue";
import CreateButton from "aleksis.core/components/generic/buttons/CreateButton.vue";
import SecondaryActionButton from "aleksis.core/components/generic/buttons/SecondaryActionButton.vue";
</script>

<template>
  <v-card
    v-if="
      !$apollo.queries.schoolStructure.loading &&
      schoolStructure?.firstLevelType?.name &&
      schoolStructure?.secondLevelType?.name
    "
    :loading="$apollo.queries.schoolStructure.loading"
  >
    <!-- Create first level group form -->
    <dialog-object-form
      v-model="createFirstLevelGroupForm"
      :fields="firstLevelGroupFields"
      :default-item="firstLevelGroupDefaultItem"
      :is-create="true"
      :gql-create-mutation="createFirstLevelGroups"
      @cancel="createFirstLevelGroupForm = false"
      @save="updateSchoolStructure"
    >
      <template #title>
        <span class="text-h5">
          {{
            $t("cursus.school_structure.add_title", {
              name: schoolStructure.firstLevelType.name,
            })
          }}
        </span>
      </template>
    </dialog-object-form>
    <!-- Create second level group form -->
    <dialog-object-form
      v-model="createSecondLevelGroupForm"
      :fields="secondLevelGroupFields"
      :default-item="secondLevelGroupDefaultItem"
      :is-create="true"
      :gql-create-mutation="createSecondLevelGroups"
      :get-create-data="transformSecondLevelGroupItem"
      @cancel="createSecondLevelGroupForm = false"
      @save="updateSchoolStructure"
    >
      <template #title>
        <span class="text-h5">
          {{
            $t("cursus.school_structure.add_title", {
              name: schoolStructure.secondLevelType.name,
            })
          }}
        </span>
      </template>
      <!-- Hide parentGroups field - it is set on first level group -->
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #parentGroups.field="{ on, attrs }">
        <input type="hidden" v-bind="attrs" v-on="on" />
      </template>
    </dialog-object-form>
    <!-- Title -->
    <div class="d-flex flex-nowrap justify-space-between">
      <div>
        <v-card-title class="text-h4">
          {{ $t("cursus.school_structure.title") }}
        </v-card-title>
      </div>
      <v-spacer />
      <div>
        <v-card-actions>
          <create-button @click="createFirstLevelGroup">
            <v-icon left>$plus</v-icon>
            {{
              $t("cursus.school_structure.add", {
                name: schoolStructure.firstLevelType.name,
              })
            }}
          </create-button>
        </v-card-actions>
      </div>
    </div>
    <!-- First level groups -->
    <v-container>
      <v-row class="overflow-x-auto flex-nowrap slide-n-snap-x-container">
        <!-- responsive 1, 2, 3, 4 col layout -->
        <v-col
          v-for="firstGroup in schoolStructure
            ? schoolStructure.firstLevelGroups
            : []"
          :key="firstGroup.id"
          class="slide-n-snap-contained"
          cols="12"
          sm="6"
          md="4"
          lg="3"
          xl="auto"
        >
          <v-card>
            <v-card-title class="justify-end">
              {{ schoolStructure.firstLevelType.name }}
              <span class="ml-3 text-h4">{{ firstGroup.shortName }}</span>
            </v-card-title>
            <v-list
              :max-height="$vuetify.breakpoint.height - 333"
              class="overflow-y-auto slide-n-snap-y-container"
            >
              <v-list-item
                v-for="secondGroup in firstGroup.childGroups"
                :key="secondGroup.id"
                class="slide-n-snap-contained"
              >
                <v-card class="mx-3 my-2">
                  <div class="d-flex flex-nowrap justify-space-between">
                    <div>
                      <v-card-title class="text-h4">
                        {{ secondGroup.shortName }}
                      </v-card-title>
                      <v-card-subtitle>
                        {{ secondGroup.name }}
                      </v-card-subtitle>
                    </div>
                    <div>
                      <v-chip-group
                        active-class="primary--text"
                        column
                        class="px-2"
                      >
                        <v-chip
                          v-for="teacher in secondGroup.owners"
                          :key="teacher.id"
                          :to="{
                            name: 'core.personById',
                            params: { id: teacher.id },
                          }"
                          outlined
                        >
                          {{ teacher.shortName || teacher.lastName }}
                        </v-chip>
                      </v-chip-group>
                      <v-card-actions>
                        <secondary-action-button
                          i18n-key="cursus.school_structure.timetable"
                          :to="{
                            name: 'lesrooster.timetable_management',
                            params: { id: secondGroup.id },
                          }"
                        />
                      </v-card-actions>
                    </div>
                  </div>
                </v-card>
              </v-list-item>
            </v-list>
            <v-card-actions>
              <v-spacer />
              <!-- MAYBE: ADD PLAN COURSES LINK -->
              <create-button
                color="secondary"
                @click="createSecondLevelGroup(firstGroup.id)"
              >
                <v-icon left>$plus</v-icon>
                {{
                  $t("cursus.school_structure.add", {
                    name: schoolStructure.secondLevelType.name,
                  })
                }}
              </create-button>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
  <error-page
    v-else
    short-error-message-key="cursus.school_structure.errors.no_group_types.short"
    long-error-message-key="cursus.school_structure.errors.no_group_types.long"
    hide-button
  />
</template>

<script>
import {
  gqlFirstLevelGroups,
  createFirstLevelGroups,
  createSecondLevelGroups,
} from "./schoolStructure.graphql";

export default {
  name: "SchoolStructure",
  data() {
    return {
      createFirstLevelGroupForm: false,
      firstLevelGroupFields: [
        {
          text: this.$t("cursus.school_structure.fields.name"),
          value: "name",
        },
        {
          text: this.$t("cursus.school_structure.fields.short_name"),
          value: "shortName",
        },
      ],
      firstLevelGroupDefaultItem: {
        name: "",
        shortName: "",
      },
      createSecondLevelGroupForm: false,
      secondLevelGroupFields: [
        {
          text: this.$t("cursus.school_structure.fields.name"),
          value: "name",
        },
        {
          text: this.$t("cursus.school_structure.fields.short_name"),
          value: "shortName",
        },
        {
          text: "NEVER SHOWN",
          value: "parentGroups",
        },
      ],
      secondLevelGroupDefaultItem: {
        name: "",
        shortName: "",
        parentGroups: [],
      },
      createSecondLevelGroupFirstLevelGroupId: 0,
    };
  },
  apollo: {
    schoolStructure: {
      query: gqlFirstLevelGroups,
    },
  },
  methods: {
    createFirstLevelGroup() {
      this.$data.createFirstLevelGroupForm = true;
    },
    createSecondLevelGroup(id) {
      this.$data.createSecondLevelGroupFirstLevelGroupId = id;
      this.$data.createSecondLevelGroupForm = true;
    },
    transformSecondLevelGroupItem(item) {
      return {
        ...item,
        parentGroups: this.$data.createSecondLevelGroupFirstLevelGroupId,
      };
    },
    updateSchoolStructure() {
      // Close both possible forms
      this.createFirstLevelGroupForm = false;
      this.createSecondLevelGroupForm = false;

      this.$apollo.queries.schoolStructure.refetch();
    },
  },
};
</script>

<style>
.slide-n-snap-x-container {
  scroll-snap-type: x mandatory;
  /* scroll-snap-stop: always; */
}
.slide-n-snap-y-container {
  scroll-snap-type: y mandatory;
  /* scroll-snap-stop: always; */
}
.slide-n-snap-contained {
  scroll-snap-align: start;
}
</style>
