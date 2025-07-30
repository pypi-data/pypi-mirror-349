<script setup>
import PositiveSmallIntegerField from "aleksis.core/components/generic/forms/PositiveSmallIntegerField.vue";
import TeacherField from "aleksis.apps.cursus/components/TeacherField.vue";
</script>

<template>
  <v-lazy
    v-model="active"
    :options="{
      threshold: 0.5,
    }"
    transition="fade-transition"
  >
    <div v-if="value.length">
      <v-row
        v-for="(course, index) in value"
        :key="index"
        no-gutters
        class="mt-2"
      >
        <v-col cols="6">
          <positive-small-integer-field
            dense
            filled
            class="mx-1"
            :disabled="loading"
            :value="
              getCurrentCourseConfig(course)
                ? getCurrentCourseConfig(course).lessonQuota
                : course.lessonQuota
            "
            :label="$t('lesrooster.timebound_course_config.lesson_quota')"
            @change="
              (event) =>
                $emit('setCourseConfigData', course, subject, header, {
                  lessonQuota: event,
                })
            "
          />
        </v-col>
        <v-col cols="6">
          <teacher-field
            dense
            filled
            class="mx-1"
            :disabled="loading"
            :label="$t('lesrooster.timebound_course_config.teachers')"
            :value="
              getCurrentCourseConfig(course)
                ? getCurrentCourseConfig(course).teachers
                : course.teachers
            "
            :show-subjects="true"
            :priority-subject="subject"
            :rules="$rules().isNonEmpty.build()"
            @input="
              (event) =>
                $emit('setCourseConfigData', course, subject, header, {
                  teachers: event,
                })
            "
          />
        </v-col>
      </v-row>
    </div>
    <div v-else>
      <v-btn
        block
        icon
        tile
        outlined
        @click="$emit('addCourse', subject.id, header.value)"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </div>
  </v-lazy>
</template>

<script>
import formRulesMixin from "aleksis.core/mixins/formRulesMixin";

export default {
  name: "TimeboundCourseConfigRasterCell",
  mixins: [formRulesMixin],
  emits: ["addCourse", "setCourseConfigData"],
  props: {
    value: {
      type: Array,
      required: true,
    },
    subject: {
      type: Object,
      required: true,
    },
    header: {
      type: Object,
      required: true,
    },
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      active: false,
    };
  },
  methods: {
    getCurrentCourseConfig(course) {
      if (course.lrTimeboundCourseConfigs?.length) {
        return course.lrTimeboundCourseConfigs[0];
      } else {
        return null;
      }
    },
  },
};
</script>
