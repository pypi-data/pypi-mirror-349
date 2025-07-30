<script setup>
import ValidityRangeField from "../validity_range/ValidityRangeField.vue";
import SubjectChip from "aleksis.apps.cursus/components/SubjectChip.vue";
import TimeboundCourseConfigRasterCell from "./TimeboundCourseConfigRasterCell.vue";
</script>

<template>
  <v-data-table
    disable-sort
    disable-filtering
    disable-pagination
    hide-default-footer
    :headers="headers"
    :items="items"
    :loading="loading"
  >
    <template #top>
      <v-row>
        <v-col
          cols="6"
          lg="3"
          class="d-flex justify-space-between flex-wrap align-center"
        >
          <v-autocomplete
            outlined
            filled
            multiple
            hide-details
            :items="groupsForPlanning"
            item-text="shortName"
            item-value="id"
            return-object
            :disabled="$apollo.queries.groupsForPlanning.loading"
            :label="$t('lesrooster.timebound_course_config.groups')"
            :loading="$apollo.queries.groupsForPlanning.loading"
            v-model="selectedGroups"
            class="mr-4"
          />
        </v-col>

        <v-col
          cols="6"
          lg="3"
          class="d-flex justify-space-between flex-wrap align-center"
        >
          <validity-range-field
            outlined
            filled
            hide-details
            v-model="internalValidityRange"
            :loading="$apollo.queries.currentValidityRange.loading"
          />
        </v-col>

        <v-col
          cols="6"
          lg="2"
          class="d-flex justify-space-between flex-wrap align-center"
        >
          <v-switch
            v-model="includeChildGroups"
            inset
            :label="
              $t(
                'lesrooster.timebound_course_config.filters.include_child_groups',
              )
            "
            :loading="$apollo.queries.subjects.loading"
          ></v-switch>
        </v-col>

        <v-spacer />
      </v-row>
    </template>

    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.subject="{ item, value }">
      <subject-chip v-if="value" :subject="value" />
    </template>

    <template
      v-for="(groupHeader, index) in groupHeaders"
      #[tableItemSlotName(groupHeader)]="{ item, value, header }"
    >
      <timebound-course-config-raster-cell
        :key="index"
        :value="value"
        :subject="item.subject"
        :header="header"
        :loading="loading"
        @addCourse="addCourse"
        @setCourseConfigData="setCourseConfigData"
      />
    </template>
  </v-data-table>
</template>

<script>
import {
  subjects,
  createTimeboundCourseConfigs,
  updateTimeboundCourseConfigs,
  createCoursesForValidityRange,
} from "./timeboundCourseConfig.graphql";

import { currentValidityRange as gqlCurrentValidityRange } from "../validity_range/validityRange.graphql";

import { gqlGroupsForPlanning } from "../helper.graphql";

import mutateMixin from "aleksis.core/mixins/mutateMixin.js";

export default {
  name: "TimeboungCourseConfigRaster",
  mixins: [mutateMixin],
  data() {
    return {
      i18nKey: "lesrooster.timebound_course_config",
      createItemI18nKey:
        "lesrooster.timebound_course_config.create_timebound_course_config",
      defaultItem: {
        course: {
          id: "",
          name: "",
        },
        validityRange: {
          id: "",
          name: "",
        },
        teachers: [],
        lessonQuota: undefined,
      },
      required: [(value) => !!value || this.$t("forms.errors.required")],
      internalValidityRange: null,
      groupsForPlanning: [],
      groups: [],
      selectedGroups: [],
      subjects: [],
      editedCourseConfigs: [],
      createdCourseConfigs: [],
      createdCourses: [],
      currentCourse: null,
      currentSubject: null,
      includeChildGroups: true,
      selectedGroupHeaders: [],
      items: [],
      groupCombinationsSet: new Set(),
    };
  },
  methods: {
    tableItemSlotName(header) {
      return "item." + header.value;
    },
    setCourseConfigData(course, subject, header, newValue) {
      // Handles input from individual raster cells.
      if (course.newCourse) {
        // No course for the given combination has been created yet.
        let existingCreatedCourse = this.createdCourses.find(
          (c) =>
            c.subject === subject.id &&
            JSON.stringify(c.groups) === header.value,
        );
        if (!existingCreatedCourse) {
          // Adds new created course object with given data.
          this.createdCourses.push({
            subject: subject.id,
            groups: JSON.parse(header.value),
            name: `${header.text}-${subject.name}`,
            ...newValue,
          });
        } else {
          // Sets given data in existing created course object.
          for (const key in newValue) {
            this.$set(existingCreatedCourse, key, newValue[key]);
          }
        }
      } else {
        // Course already exists.
        if (!course.lrTimeboundCourseConfigs?.length) {
          // No TCCs exist for given course.
          let existingCreatedCourseConfig = this.createdCourseConfigs.find(
            (c) =>
              c.course === course.id &&
              c.validityRange === this.internalValidityRange?.id,
          );
          if (!existingCreatedCourseConfig) {
            // Adds new TCC object with given data.
            this.createdCourseConfigs.push({
              course: course.id,
              validityRange: this.internalValidityRange?.id,
              teachers: course.teachers.map((t) => t.id),
              lessonQuota: course.lessonQuota,
              ...newValue,
            });
          } else {
            // Sets given data in existing TCC object.
            for (const key in newValue) {
              this.$set(existingCreatedCourseConfig, key, newValue[key]);
            }
          }
        } else {
          // TCC already exists
          let courseConfigID = course.lrTimeboundCourseConfigs[0].id;
          let existingEditedCourseConfig = this.editedCourseConfigs.find(
            (c) => c.id === courseConfigID,
          );
          if (!existingEditedCourseConfig) {
            // Adds new object representing edits made to existing TCC.
            this.editedCourseConfigs.push({ id: courseConfigID, ...newValue });
          } else {
            // Sets given data in existing TCC edit object.
            for (const key in newValue) {
              this.$set(existingEditedCourseConfig, key, newValue[key]);
            }
          }
        }
      }
    },
    updateCourseConfigs(cachedSubjects, incomingCourseConfigs) {
      // Handles incoming TCCs on partial update after mutation.
      // Find related existing course by subject and course ID.
      incomingCourseConfigs.forEach((newCourseConfig) => {
        const subject = cachedSubjects.find(
          (s) => s.id === newCourseConfig.course.subject.id,
        );
        if (!subject) {
          return;
        }

        const course = subject.courses.find(
          (c) => c.id === newCourseConfig.course.id,
        );

        course.lrTimeboundCourseConfigs = [newCourseConfig];
      });

      return cachedSubjects;
    },
    updateCreatedCourses(cachedSubjects, incomingCourses) {
      // Handles incoming courses on partial update after mutation.
      // Insert course into existing data by subject ID.
      incomingCourses.forEach((newCourse) => {
        const subject = cachedSubjects.find(
          (s) => s.id === newCourse.subject.id,
        );
        if (!subject) {
          return;
        }

        subject.courses.push(newCourse);
      });

      return cachedSubjects;
    },
    addCourse(subject, groups) {
      // Handles clicks on "+" button.
      // Adds course for given subject/groups combination and marks it as newly created.
      this.$set(
        this.items.find((i) => i.subject.id === subject),
        groups,
        [{ teachers: [], newCourse: true }],
      );
    },
    generateTableItems(subjects) {
      // Generates items for data table, sorted by subjects.
      const subjectsWithSortedCourses = subjects.map((subject) => {
        let { courses, ...reducedSubject } = subject;
        let groupCombinations = {};

        courses.forEach((course) => {
          // Aggregates all relevant group IDs.
          const ownGroupIDs = course.groups.map((group) => group.id);
          let groupIDs;

          // If child groups should be included, add them.
          if (
            this.includeChildGroups &&
            ownGroupIDs.some((groupID) => !this.groupIDSet.has(groupID))
          ) {
            groupIDs = JSON.stringify(
              course.groups
                .flatMap((group) =>
                  group.parentGroups.map((parentGroup) => parentGroup.id),
                )
                .sort(),
            );
          } else {
            groupIDs = JSON.stringify(ownGroupIDs.sort());
          }

          // Based on stringified aggregated groups, add group combination entry for subject.
          if (!groupCombinations[groupIDs]) {
            groupCombinations[groupIDs] = [];
            if (course.groups.length > 1) {
              this.groupCombinationsSet.add(groupIDs);
            }
            groupCombinations[groupIDs].push({
              ...course,
            });
          } else if (
            !groupCombinations[groupIDs].some((c) => c.id === course.id)
          ) {
            groupCombinations[groupIDs].push({
              ...course,
            });
          }
        });

        return {
          subject: reducedSubject,
          ...Object.fromEntries(
            this.groupHeaders.map((header) => [header.value, []]),
          ),
          ...groupCombinations,
        };
      });
      return subjectsWithSortedCourses;
    },
  },
  computed: {
    groupIDSet() {
      // Group ID set without duplicates.
      return new Set(this.selectedGroups.map((group) => group.id));
    },
    groupCombinationHeaders() {
      // Generates additional table headers based on unique group combinations found from existing courses.
      return this.subjectGroupCombinations.map((combination) => {
        let parsedCombination = JSON.parse(combination);
        return {
          text: parsedCombination
            .map(
              (groupID) =>
                this.selectedGroups.find((group) => group.id === groupID)
                  ?.shortName ||
                this.selectedGroups.find((group) => group.id === groupID)
                  ?.shortName,
            )
            .join(", "),
          value: combination,
        };
      });
    },
    groupHeaders() {
      return [...this.selectedGroupHeaders, ...this.groupCombinationHeaders];
    },
    headers() {
      let groupHeadersWithWidth = this.groupHeaders.map((header) => ({
        ...header,
        width: "20vw",
      }));
      // Adds column for subjects.
      return [
        {
          text: this.$t("lesrooster.timebound_course_config.subject"),
          value: "subject",
          width: "5%",
        },
      ].concat(groupHeadersWithWidth);
    },
    subjectGroupCombinations() {
      return Array.from(this.groupCombinationsSet);
    },
    createdCoursesReady() {
      // Indicates whether local created course data is ready to be used in mutation.
      return (
        !!this.createdCourses.length &&
        this.createdCourses.every((c) => {
          return (
            c?.groups?.length && c.name && c.subject && c?.teachers?.length
          );
        })
      );
    },
    createdCourseConfigsReady() {
      // Indicates whether local created TCCs data is ready to be used in mutation.
      return (
        !!this.createdCourseConfigs.length &&
        this.createdCourseConfigs.every((c) => {
          return c.course && c.validityRange && c?.teachers?.length;
        })
      );
    },
    editedCourseConfigsReady() {
      // Indicates whether local edited TCCs data is ready to be used in mutation.
      return (
        !!this.editedCourseConfigs.length &&
        this.editedCourseConfigs.every((c) => {
          return (
            c.id && (Object.hasOwn(c, "lessonQuota") || c?.teachers?.length)
          );
        })
      );
    },
    expandedQuery() {
      return {
        ...this.$apollo.queries.subjects.options,
        variables: JSON.parse(
          this.$apollo.queries.subjects.previousVariablesJson,
        ),
      };
    },
    tableLoading() {
      return (
        this.loading ||
        this.$apollo.queries.subjects.loading ||
        this.$apollo.queries.groupsForPlanning.loading ||
        this.$apollo.queries.currentValidityRange.loading
      );
    },
  },
  watch: {
    selectedGroups(newValue) {
      this.selectedGroupHeaders = newValue.map((group) => ({
        text: group.shortName,
        value: JSON.stringify([group.id]),
      }));
    },
    editedCourseConfigs: {
      deep: true,
      handler(newValue) {
        if (this.editedCourseConfigsReady) {
          this.mutate(
            updateTimeboundCourseConfigs,
            {
              input: newValue,
            },
            this.updateCourseConfigs,
          );

          this.editedCourseConfigs = [];
        }
      },
    },
    createdCourseConfigs: {
      deep: true,
      handler(newValue) {
        if (this.createdCourseConfigsReady) {
          this.mutate(
            createTimeboundCourseConfigs,
            {
              input: newValue,
            },
            this.updateCourseConfigs,
          );

          this.createdCourseConfigs = [];
        }
      },
    },
    createdCourses: {
      deep: true,
      handler(newValue) {
        if (this.createdCoursesReady) {
          this.mutate(
            createCoursesForValidityRange,
            {
              input: newValue,
              validityRange: this.internalValidityRange.id,
            },
            this.updateCreatedCourses,
          );

          this.createdCourses = [];
        }
      },
    },
  },
  apollo: {
    currentValidityRange: {
      query: gqlCurrentValidityRange,
      result({ data }) {
        if (!data) return;
        this.internalValidityRange = data.currentValidityRange;
      },
    },
    groupsForPlanning: {
      query: gqlGroupsForPlanning,
      result({ data }) {
        if (!data) return;
        this.selectedGroups = data.groupsForPlanning;
      },
    },
    subjects: {
      query: subjects,
      skip() {
        return !this.groupIDSet.size || !this.internalValidityRange;
      },
      variables() {
        return {
          groups: Array.from(this.groupIDSet),
          includeChildGroups: this.includeChildGroups,
        };
      },
      update: (data) => data.items,
      result({ data }) {
        if (!data) return;
        this.items = this.generateTableItems(data.items);
      },
    },
  },
};
</script>

<style scoped></style>
