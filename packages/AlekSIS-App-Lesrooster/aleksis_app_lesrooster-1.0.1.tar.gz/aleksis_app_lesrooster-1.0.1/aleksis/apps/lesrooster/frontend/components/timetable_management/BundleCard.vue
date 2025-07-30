<script>
import { defineComponent } from "vue";
import ColoredShortNameChip from "../common/ColoredShortNameChip.vue";

import bundleAccessorsMixin from "../../mixins/bundleAccessorsMixin.js";

export default defineComponent({
  name: "BundleCard",
  components: { ColoredShortNameChip },
  mixins: [bundleAccessorsMixin],
  extends: "v-card",
  props: {
    /**
     * Bundle to show
     * @values CourseBundle, LessonBundle
     */
    bundle: {
      type: Object,
      required: true,
    },
    highlightedTeachers: {
      type: Array,
      required: false,
      default: () => [],
    },
    highlightedRooms: {
      type: Array,
      required: false,
      default: () => [],
    },
    oneLine: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  computed: {
    children() {
      return this.bundleChildren(this.bundle);
    },
    subjects() {
      return this.bundleSubjects(this.bundle).map(
        (subject) =>
          subject || {
            name: "",
            colourFg: "#000000",
            colourBg: "#e6e6e6",
          },
      );
    },
    teachers() {
      return this.bundleTeachers(this.bundle);
    },
    rooms() {
      return this.bundleRooms(this.bundle);
    },
    outlined() {
      return this.subjects.length > 1;
    },
    colorFg() {
      if (this.subjects.length === 1) {
        return this.subjects[0].colourFg;
      } else {
        return this.$vuetify.theme.currentTheme.primary;
      }
    },
    colorBg() {
      if (this.subjects.length === 1) {
        return this.subjects[0].colourBg;
      } else {
        return null;
      }
    },
    loading() {
      return (
        this.bundle.isOptimistic ||
        this.bundle.id.toString().startsWith("temporary")
      );
    },
  },
});
</script>

<template>
  <v-card
    :color="colorBg"
    :outlined="outlined"
    :disabled="loading"
    :style="{ 'border-color': colorFg }"
    class="color no-select h-100 fill-height d-flex align-center justify-center pa-0 width-title"
    v-bind="$attrs"
    v-on="$listeners"
  >
    <div
      v-if="!loading"
      :class="{ 'd-flex align-center my-1': true, 'flex-column': !oneLine }"
    >
      <component
        :is="oneLine ? 'div' : 'v-card-title'"
        class="color d-flex justify-center flex-wrap px-3 py-0 ma-0"
      >
        <!-- Show subject shortname with full course name as tooltip. -->
        <v-tooltip v-for="child in children" :key="child.id" bottom tag="span">
          <template #activator="{ on, attrs }">
            <span v-bind="attrs" v-on="on" class="separator-after-first">
              {{ child.subject.shortName }}
            </span>
          </template>
          <span>{{ child.name || child.course.name }}</span>
        </v-tooltip>

        <!-- Show full course name as subtitle if enough space and bundle of one. -->
        <v-card-subtitle
          v-if="children.length === 1"
          class="caption px-3 py-0 ma-0 text-center hidden-when-small"
        >
          {{ children[0].name || children[0].course.name }}
        </v-card-subtitle>
      </component>

      <!-- Show teachers -->
      <v-card-subtitle
        class="color pa-0 ma-0 d-flex flex-wrap justify-center small-gap"
      >
        <span v-for="teacher in teachers" :key="'teacher-' + teacher.id">
          <v-tooltip bottom>
            <template #activator="{ on, attrs }">
              <colored-short-name-chip
                :default-color="[colorFg, colorBg, true]"
                :override-color="!highlightedTeachers.includes(teacher.id)"
                v-bind="attrs"
                v-on="on"
                @click="$emit('click:teacher', teacher)"
                :item="teacher"
                :elevation="0"
              />
            </template>
            <span>{{ teacher.fullName }}</span>
          </v-tooltip>
        </span>
        <!-- Show rooms -->
        <span v-for="room in rooms" :key="'room-' + room.id">
          <v-tooltip bottom>
            <template #activator="{ on, attrs }">
              <colored-short-name-chip
                :default-color="[colorFg, colorBg, true]"
                :override-color="!highlightedRooms.includes(room.id)"
                v-bind="attrs"
                v-on="on"
                @click="$emit('click:room', room)"
                :item="room"
                :elevation="0"
              />
            </template>
            <span>{{ room.name }}</span>
          </v-tooltip>
        </span>
      </v-card-subtitle>
      <slot />
    </div>
    <div v-if="loading" class="text-center">
      <v-progress-circular :color="colorFg" indeterminate />
    </div>
  </v-card>
</template>

<style scoped>
.width-title {
  container: title/inline-size;
}

.hidden-when-small {
  display: none;
}

@container title (width > 150px) {
  .hidden-when-small {
    display: inline;
  }
}

.color {
  color: v-bind(colorFg);
}

.no-select {
  user-select: none;
}

.small-gap {
  gap: 0.25rem;
}

.separator-after-first:not(:first-of-type)::before {
  content: "·";
  padding-left: 0.25em;
}
</style>
