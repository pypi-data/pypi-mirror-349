<script setup>
import TimetableWrapper from "aleksis.apps.chronos/components/TimetableWrapper.vue";
import TimeGridField from "../validity_range/TimeGridField.vue";
import RoomTimeTable from "./RoomTimeTable.vue";
import GroupTimeTable from "./GroupTimeTable.vue";
import TeacherTimeTable from "./TeacherTimeTable.vue";
</script>
<script>
export default {
  name: "Timetable",
  data() {
    return {
      timeGrid: null,
      selected: null,
    };
  },
  watch: {
    timeGrid(newTimeGrid) {
      this.onSelected(this.selected);
    },
  },
  computed: {
    timetableAttrs() {
      return {
        id: this.$route.params.id,
        timeGrid: this.timeGrid,
      };
    },
  },
  methods: {
    onSelected(selected) {
      this.selected = selected;
      if (!selected && this.timeGrid) {
        this.$router.push({
          name: "lesrooster.timetableWithTimeGrid",
          params: { timeGrid: this.timeGrid.id },
        });
      } else if (!selected && !this.timeGrid) {
        this.$router.push({ name: "lesrooster.timetable" });
      } else if (
        selected.objId !== this.$route.params.id ||
        selected.type.toLowerCase() !== this.$route.params.type ||
        this.timeGrid.id !== this.$route.params.timeGrid
      ) {
        this.$router.push({
          name: "lesrooster.timetableWithId",
          params: {
            timeGrid: this.timeGrid.id,
            type: selected.type.toLowerCase(),
            id: selected.objId,
          },
        });
      }
    },
    setInitialTimeGrid(timeGrids) {
      if (!this.timeGrid) {
        this.timeGrid = timeGrids.find(
          this.$route.params.timeGrid
            ? (timeGrid) => timeGrid.id === this.$route.params.timeGrid
            : (timeGrid) => timeGrid.validityRange.isCurrent && !timeGrid.group,
        );
      }
    },
  },
};
</script>

<template>
  <timetable-wrapper :on-selected="onSelected">
    <template #additionalSelect="{ selected, mobile }">
      <v-card
        :class="{ 'mb-2': !mobile, 'mx-2 mt-2': mobile }"
        :outlined="mobile"
      >
        <v-card-text>
          <time-grid-field
            outlined
            filled
            :label="$t('lesrooster.labels.select_validity_range')"
            hide-details
            with-dates
            :enable-create="false"
            v-model="timeGrid"
            @items="setInitialTimeGrid"
          >
          </time-grid-field>
        </v-card-text>
      </v-card>
    </template>
    <template #additionalButton="{ selected, mobile }">
      <div :class="{ 'full-width': mobile, 'd-flex': true }" v-if="selected">
        <v-btn
          outlined
          color="secondary"
          small
          :class="{ 'mx-3 flex-grow-1': true, 'mb-3': mobile }"
          :to="{
            name: 'lesrooster.timetablePrint',
            params: {
              timeGrid: timeGrid.id,
              type: selected.type.toLowerCase(),
              id: selected.objId,
            },
          }"
          target="_blank"
        >
          <v-icon left>mdi-printer-outline</v-icon>
          {{ $t("lesrooster.timetable.print") }}
        </v-btn>
      </div>
    </template>
    <template #default="{ selected }">
      <group-time-table
        v-if="$route.params.type === 'group'"
        v-bind="timetableAttrs"
      />
      <teacher-time-table
        v-else-if="$route.params.type === 'teacher'"
        v-bind="timetableAttrs"
      />
      <room-time-table
        v-else-if="$route.params.type === 'room'"
        v-bind="timetableAttrs"
      />
    </template>
  </timetable-wrapper>
</template>
