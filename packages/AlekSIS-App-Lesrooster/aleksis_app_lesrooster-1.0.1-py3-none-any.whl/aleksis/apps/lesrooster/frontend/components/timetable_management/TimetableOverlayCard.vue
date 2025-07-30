<script>
import BlockingCard from "./BlockingCard.vue";
import ColoredShortNameChip from "../common/ColoredShortNameChip.vue";

import bundleAccessorsMixin from "../../mixins/bundleAccessorsMixin.js";

export default {
  name: "TimetableOverlayCard",
  components: { ColoredShortNameChip, BlockingCard },
  mixins: [bundleAccessorsMixin],
  props: {
    bundle: {
      type: Object,
      required: true,
    },
    weekdays: {
      type: Array,
      required: true,
    },
    periods: {
      type: Array,
      required: true,
    },
    draggedItem: {
      type: Object,
      required: true,
    },
  },
  computed: {
    x() {
      return this.weekdays.indexOf(this.bundle.slotStart.weekday) + 1;
    },
    y() {
      return this.periods.indexOf(this.bundle.slotStart.period) + 1;
    },
    w() {
      return (
        this.weekdays.indexOf(this.bundle.slotEnd.weekday) -
        this.weekdays.indexOf(this.bundle.slotStart.weekday) +
        1
      );
    },
    h() {
      return (
        this.periods.indexOf(this.bundle.slotEnd.period) -
        this.periods.indexOf(this.bundle.slotStart.period) +
        1
      );
    },
    rooms() {
      const selectedRooms = this.bundleRooms(this.draggedItem).map(
        (room) => room.id,
      );
      return this.bundleRooms(this.bundle)?.filter((room) =>
        selectedRooms.includes(room.id),
      );
    },
    teachers() {
      const selectedTeachers = this.bundleTeachers(this.draggedItem).map(
        (teacher) => teacher.id,
      );
      return this.bundleTeachers(this.bundle)?.filter((teacher) =>
        selectedTeachers.includes(teacher.id),
      );
    },
  },
};
</script>

<template>
  <div>
    <blocking-card
      v-for="room in rooms"
      icon="mdi-home-off-outline"
      color="warning"
      :key="'room-' + room.id"
    >
      <colored-short-name-chip class="short" :item="room" :elevation="0" />
    </blocking-card>
    <blocking-card
      v-for="teacher in teachers"
      icon="mdi-account-off-outline"
      color="warning"
      :key="'teacher-' + teacher.id"
    >
      <colored-short-name-chip class="short" :item="teacher" :elevation="0" />
    </blocking-card>
  </div>
</template>

<style scoped>
div {
  grid-column: v-bind(x) / span v-bind(w);
  grid-row: v-bind(y) / span v-bind(h);
  z-index: 10;
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  gap: 5px;
  width: 100%;
  height: 100%;
}
</style>
