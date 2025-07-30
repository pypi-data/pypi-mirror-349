<script>
import { defineComponent } from "vue";
import {
  courseBundles,
  createLessonBundles,
  deleteLessonBundles,
  gqlGroupsByTimeGrid,
  lessonBundles,
  moveLessonBundles,
  overlayBundles,
  updateLessons,
} from "./timetableManagement.graphql";
import { gqlTeachers } from "../helper.graphql";
import { timeGrids } from "../validity_range/validityRange.graphql";
import { slots } from "../breaks_and_slots/slot.graphql";
import { rooms } from "aleksis.core/components/room/room.graphql";
import MobileFullscreenDialog from "aleksis.core/components/generic/dialogs/MobileFullscreenDialog.vue";
import DeleteDialog from "aleksis.core/components/generic/dialogs/DeleteDialog.vue";
import DialogObjectForm from "aleksis.core/components/generic/dialogs/DialogObjectForm.vue";
import SecondaryActionButton from "aleksis.core/components/generic/buttons/SecondaryActionButton.vue";
import SubjectField from "aleksis.apps.cursus/components/SubjectField.vue";
import BundleCard from "./BundleCard.vue";

import { RRule } from "rrule";
import TeacherTimeTable from "../timetables/TeacherTimeTable.vue";
import RoomTimeTable from "../timetables/RoomTimeTable.vue";
import LessonRatioChip from "./LessonRatioChip.vue";
import TimeGridField from "../validity_range/TimeGridField.vue";
import BlockingCard from "./BlockingCard.vue";
import PeriodCard from "./PeriodCard.vue";
import TimetableOverlayCard from "./TimetableOverlayCard.vue";

import bundleAccessorsMixin from "../../mixins/bundleAccessorsMixin.js";

export default defineComponent({
  name: "TimetableManagement",
  components: {
    TimetableOverlayCard,
    PeriodCard,
    BlockingCard,
    TimeGridField,
    SubjectField,
    DialogObjectForm,
    LessonRatioChip,
    MobileFullscreenDialog,
    RoomTimeTable,
    TeacherTimeTable,
    DeleteDialog,
    BundleCard,
    SecondaryActionButton,
  },
  mixins: [bundleAccessorsMixin],
  data() {
    return {
      weekdays: [],
      periods: [],
      slotsByPeriods: [],
      internalTimeGrid: null,
      courseSearch: null,
      lessonsUsed: {},
      lessonQuotaTotal: 0,
      deleteMutation: deleteLessonBundles,
      deleteDialog: false,
      itemsToDelete: [],
      selectedObject: null,
      selectedObjectType: null,
      selectedObjectTitle: "",
      selectedObjectDialogOpen: false,
      selectedObjectDialogTab: 0,
      timeGrids: [],
      groups: [],
      selectedGroup: null,
      lessonEdit: {
        open: false,
        id: null,
        object: {},
        fields: [
          {
            text: this.$t(
              "lesrooster.timetable_management.lesson_fields.subject",
            ),
            value: "subject",
          },
          {
            text: this.$t(
              "lesrooster.timetable_management.lesson_fields.teachers",
            ),
            value: "teachers",
          },
          {
            text: this.$t(
              "lesrooster.timetable_management.lesson_fields.rooms",
            ),
            value: "rooms",
          },
        ],
        mutation: updateLessons,
      },
      draggedItem: null,
      overlayBundles: [],
    };
  },
  apollo: {
    groups: {
      query: gqlGroupsByTimeGrid,
      variables() {
        return {
          timeGrid: this.internalTimeGrid.id,
        };
      },
      skip() {
        return this.internalTimeGrid?.id == null;
      },
      result() {
        if (this.$route.params.group && this.groups) {
          this.selectedGroup = this.groups.find(
            (group) => group.id === this.$route.params.group,
          );
        }
      },
    },
    slots: {
      query: slots,
      variables() {
        return {
          filters: JSON.stringify({
            time_grid: this.internalTimeGrid.id,
          }),
        };
      },
      skip() {
        return !this.readyForQueries;
      },
      update: (data) => data.items,
      result({ data: { items } }) {
        this.weekdays = Array.from(
          new Set(
            items
              .filter((slot) => slot.model === "Slot")
              .map((slot) => slot.weekday),
          ),
        );
        this.periods = Array.from(
          new Set(
            items
              .filter((slot) => slot.model === "Slot")
              .map((slot) => slot.period),
          ),
        );
        this.slotsByPeriods = this.periods.map((period) => ({
          period: period,
          slots: items.filter(
            (slot) => slot.model === "Slot" && slot.period === period,
          ),
        }));
      },
    },
    timeGrids: {
      query: timeGrids,
      update: (data) => data.items,
      variables() {
        return {
          filters: JSON.stringify({
            validity_range: this.internalTimeGrid.validityRange.id,
          }),
        };
      },
      skip() {
        return !this.internalTimeGrid;
      },
    },
    courseBundles: {
      query: courseBundles,
      variables() {
        return {
          group: this.selectedGroup.id,
          validityRange: this.internalTimeGrid.validityRange.id,
        };
      },
      skip() {
        return !this.readyForQueries;
      },
      result({ data }) {
        this.lessonQuotaTotal =
          data && data.courseBundles
            ? data.courseBundles.reduce(
                (accumulator, course) => accumulator + course.lessonQuota,
                0,
              )
            : 0;
      },
    },
    lessonBundles: {
      query: lessonBundles,
      variables() {
        return {
          group: this.selectedGroup.id,
          timeGrid: this.internalTimeGrid.id,
        };
      },
      skip() {
        return !this.readyForQueries;
      },
      result({ data }) {
        this.lessonsUsed = {};
        data.lessonBundles.forEach((lessonBundle) => {
          let increment =
            this.periods.indexOf(lessonBundle.slotEnd.period) -
            this.periods.indexOf(lessonBundle.slotStart.period) +
            1;
          this.lessonsUsed[lessonBundle.courseBundle.id] =
            this.lessonsUsed[lessonBundle.courseBundle.id] + increment ||
            increment;
        });
      },
    },
    overlayBundles: {
      query: overlayBundles,
      variables() {
        return {
          timeGrid: this.internalTimeGrid.id,
          rooms: this.draggedRooms,
          teachers: this.draggedTeachers,
        };
      },
      skip() {
        return !this.readyForQueries || !this.draggedItem;
      },
    },
    persons: {
      query: gqlTeachers,
    },
    rooms: {
      query: rooms,
      update: (data) => data.items,
    },
  },
  computed: {
    readyForQueries() {
      // Non-typesafe check to also handle undefined
      return (
        this.internalTimeGrid != null &&
        this.selectedGroup != null &&
        this.selectedGroup.id != null
      );
    },
    griddedLessonBundles() {
      return this.lessonBundles
        ? this.lessonBundles.map((lessonBundle) => ({
            x: this.weekdays.indexOf(lessonBundle.slotStart.weekday) + 1,
            y: this.periods.indexOf(lessonBundle.slotStart.period) + 1,
            w:
              this.weekdays.indexOf(lessonBundle.slotEnd.weekday) -
              this.weekdays.indexOf(lessonBundle.slotStart.weekday) +
              1,
            h:
              this.periods.indexOf(lessonBundle.slotEnd.period) -
              this.periods.indexOf(lessonBundle.slotStart.period) +
              1,
            key: "lesson-bundle-" + lessonBundle.id,
            disabled: !lessonBundle.canEdit,
            data: lessonBundle,
          }))
        : [];
    },
    gridItems() {
      // As we may want to display more in the future
      return this.griddedLessonBundles;
    },
    gridLoading() {
      return (
        this.$apollo.queries.slots.loading ||
        this.$apollo.queries.lessonBundles.loading ||
        this.$apollo.queries.groups.loading
      );
    },
    griddedCourseBundles() {
      return this.courseBundles
        ? this.courseBundles.map((bundle) => {
            const lessonQuota =
              bundle.lessonQuota ||
              bundle.courses.reduce(
                (min, course) => Math.min(min, course.lessonQuota),
                Number.MAX_SAFE_INTEGER,
              );
            return {
              x: "0",
              y: "0",
              w: 1,
              h: 1,
              key: "course-bundle-" + bundle.id,
              data: {
                // TODO: A uniform interface between courseBundles and lessonBundles
                ...bundle,
                lessonQuota: lessonQuota,
                lessonsUsed: this.lessonsUsed[bundle.id] || 0,
                lessonRatio: (this.lessonsUsed[bundle.id] || 0) / lessonQuota,
              },
            };
          })
        : [];
    },
    disabledSlots() {
      // Disable all fields in the grid where no slot exists
      return this.periods
        .map((period, indexY) =>
          this.weekdays.map((weekday, indexX) =>
            this.slots.filter(
              (slot) =>
                slot.model === "Slot" &&
                slot.weekday === weekday &&
                slot.period === period,
            ).length === 0
              ? {
                  x: indexX + 1,
                  y: indexY + 1,
                }
              : undefined,
          ),
        )
        .flat()
        .filter((val) => val !== undefined);
    },
    totalLessonRatio() {
      return this.$t(
        "lesrooster.timetable_management.lessons_used_ratio_total",
        {
          lessonsUsed: Object.values(this.lessonsUsed).reduce(
            (a, b) => a + b,
            0,
          ),
          lessonQuota: this.lessonQuotaTotal,
        },
      );
    },
    draggedTeachers() {
      const bundle = this.draggedItem?.data;
      if (bundle) {
        return this.bundleTeachers(bundle).map((teacher) => teacher.id);
      }
      return [];
    },
    draggedRooms() {
      const bundle = this.draggedItem?.data;
      if (bundle) {
        return this.bundleRooms(bundle).map((room) => room.id);
      }
      return [];
    },
  },
  watch: {
    selectedGroup() {
      if (!this.selectedGroup) return;
      if (
        this.selectedGroup.id != this.$route.params.group ||
        this.internalTimeGrid.id != this.$route.params.timeGrid
      ) {
        // to be able to select a group, the timeGrid has to be set
        this.$router.push({
          name: "lesrooster.timetable_management",
          params: {
            group: this.selectedGroup.id,
            timeGrid: this.internalTimeGrid.id,
          },
        });
      }
      this.$setToolBarTitle(
        this.$t("lesrooster.timetable_management.for_group", {
          group: this.selectedGroup.name,
        }),
      );
      this.$apollo.queries.courseBundles.refetch();
      this.$apollo.queries.lessonBundles.refetch();
    },
    internalTimeGrid(newTimeGrid, oldTimeGrid) {
      if (!oldTimeGrid) return;

      if (this.selectedGroup?.id) {
        this.$router.push({
          name: "lesrooster.timetable_management",
          params: {
            group: this.selectedGroup.id,
            timeGrid: this.internalTimeGrid.id,
          },
        });
      }
    },
  },
  methods: {
    itemMovedToLessons(eventData) {
      let newStartSlotId = this.slots.filter(
        (slot) =>
          slot.period === this.periods[eventData.y - 1] &&
          slot.weekday === this.weekdays[eventData.x - 1],
      );
      let newEndSlotId = this.slots.filter(
        (slot) =>
          slot.period === this.periods[eventData.y + eventData.h - 2] &&
          slot.weekday === this.weekdays[eventData.x + eventData.w - 2],
      );

      let newStartSlot, newEndSlot;

      if (newStartSlotId.length === 1 && newStartSlotId.length === 1) {
        newStartSlot = newStartSlotId[0];
        newStartSlotId = newStartSlot.id;

        newEndSlot = newEndSlotId[0];
        newEndSlotId = newEndSlot.id;
      } else {
        throw new Error("Multiple slots matched");
      }

      if (eventData.originGridId === "lessonBundles") {
        let that = this;
        this.$apollo
          .mutate({
            mutation: moveLessonBundles,
            variables: {
              input: {
                id: eventData.data.id,
                slotStart: newStartSlotId,
                slotEnd: newEndSlotId,
              },
            },
            optimisticResponse: {
              updateLessonBundles: {
                lessonBundles: [
                  {
                    ...eventData.data,
                    slotStart: newStartSlot,
                    slotEnd: newEndSlot,
                    isOptimistic: true,
                  },
                ],
                __typename: "LessonBundleBatchPatchMutation",
              },
            },
            update(
              store,
              {
                data: {
                  updateLessonBundles: { lessonBundles },
                },
              },
            ) {
              let query = {
                ...that.$apollo.queries.lessonBundles.options,
                variables: JSON.parse(
                  that.$apollo.queries.lessonBundles.previousVariablesJson,
                ),
              };
              // Read the data from cache for query
              const storedData = store.readQuery(query);

              if (!storedData) {
                // There are no data in the cache yet
                return;
              }

              lessonBundles.forEach((lessonBundle) => {
                const index = storedData.lessonBundles.findIndex(
                  (lessonBundleObject) =>
                    lessonBundleObject.id === lessonBundle.id,
                );
                storedData.lessonBundles[index].slotStart =
                  lessonBundle.slotStart;
                storedData.lessonBundles[index].slotEnd = lessonBundle.slotEnd;

                // Write data back to the cache
                store.writeQuery({ ...query, data: storedData });
              });
            },
          })
          .then(() => {
            this.$toastSuccess(
              this.$t(
                "lesrooster.timetable_management.snacks.lesson_move.success",
              ),
            );
          })
          .catch(() => {
            this.$toastError(
              this.$t(
                "lesrooster.timetable_management.snacks.lesson_move.error",
              ),
            );
          });
      } else if (eventData.originGridId === "courseBundles") {
        let that = this;
        const rule = new RRule({
          freq: RRule.WEEKLY, // TODO: Make this configurable
          dtstart: new Date(this.internalTimeGrid.validityRange.dateStart), // FIXME: check if this is correct with timezones etc.
          until: new Date(this.internalTimeGrid.validityRange.dateEnd), // FIXME: check if this is correct with timezones etc.
        });
        const recurrenceString = rule.toString();
        this.$apollo
          .mutate({
            mutation: createLessonBundles,
            variables: {
              input: {
                slotStart: newStartSlotId,
                slotEnd: newEndSlotId,
                courseBundle: eventData.data.id,
                recurrence: recurrenceString,
              },
            },
            optimisticResponse: {
              createLessonBundles: {
                items: [
                  {
                    id: "temporary-lesson-bundle-id-" + crypto.randomUUID(),
                    slotStart: newStartSlot,
                    slotEnd: newEndSlot,
                    recurrence: recurrenceString,
                    courseBundle: eventData.data,
                    lessons: eventData.data.courses.map((course) => {
                      return {
                        id: "temporary-lesson-id-" + crypto.randomUUID(),
                        course: course,
                        rooms: [course.defaultRoom],
                        teachers: course.teachers,
                        subject: course.subject,
                        __typename: "LessonType",
                      };
                    }),
                    isOptimistic: true,
                    canEdit: true,
                    canDelete: true,
                    __typename: "LessonBundleType",
                  },
                ],
                __typename: "LessonBundleBatchCreateMutation",
              },
            },
            update(
              store,
              {
                data: {
                  createLessonBundles: { items },
                },
              },
            ) {
              let query = {
                ...that.$apollo.queries.lessonBundles.options,
                variables: JSON.parse(
                  that.$apollo.queries.lessonBundles.previousVariablesJson,
                ),
              };
              // Read the data from cache for query
              const storedData = store.readQuery(query);

              if (!storedData) {
                // There are no data in the cache yet
                return;
              }

              items.forEach((lessonBundle) =>
                storedData.lessonBundles.push(lessonBundle),
              );

              // Write data back to the cache
              store.writeQuery({ ...query, data: storedData });
            },
          })
          .then(() => {
            this.$toastSuccess(
              this.$t(
                "lesrooster.timetable_management.snacks.lesson_create.success",
              ),
            );
          })
          .catch(() => {
            this.$toastError(
              this.$t(
                "lesrooster.timetable_management.snacks.lesson_create.error",
              ),
            );
          });
      }
    },
    itemMovedToCourses(eventData) {
      if (eventData.originGridId === "lessonBundles") {
        // TODO: remove lessons from plan?
        // Maybe not needed, due to delete button in menu
      }
    },
    canShortenLessonBundle(lessonBundle) {
      // Only allow shortening a lessonBundle if it is longer than 1 slot
      return lessonBundle.slotEnd.id !== lessonBundle.slotStart.id;
    },
    canProlongLessonBundle(lessonBundle) {
      const nextSlot = this.slots
        .filter(
          (slot) =>
            slot.weekday === lessonBundle.slotEnd.weekday &&
            slot.period > lessonBundle.slotEnd.period,
        )
        .reduce(
          (prev, current) =>
            prev && prev.period > current.period ? current : prev || current,
          null,
        );

      return !!nextSlot;
    },
    changeLessonBundleSlots(lessonBundle, slotStart, slotEnd) {
      let that = this;
      this.$apollo
        .mutate({
          mutation: moveLessonBundles,
          variables: {
            input: {
              id: lessonBundle.id,
              slotStart: slotStart.id,
              slotEnd: slotEnd.id,
            },
          },
          optimisticResponse: {
            updateLessonBundles: {
              lessonBundles: [
                {
                  ...lessonBundle,
                  slotStart: slotStart,
                  slotEnd: slotEnd,
                  isOptimistic: true,
                },
              ],
              __typename: "LessonBundleBatchPatchMutation",
            },
          },
          update(
            store,
            {
              data: {
                updateLessonBundles: { lessonBundles },
              },
            },
          ) {
            let query = {
              ...that.$apollo.queries.lessonBundles.options,
              variables: JSON.parse(
                that.$apollo.queries.lessonBundles.previousVariablesJson,
              ),
            };
            // Read the data from cache for query
            const storedData = store.readQuery(query);

            if (!storedData) {
              // There are no data in the cache yet
              return;
            }

            lessonBundles.forEach((lessonBundle) => {
              const index = storedData.lessonBundles.findIndex(
                (lessonBundleObject) =>
                  lessonBundleObject.id === lessonBundle.id,
              );
              storedData.lessonBundles[index].slotStart =
                lessonBundle.slotStart;
              storedData.lessonBundles[index].slotEnd = lessonBundle.slotEnd;

              // Write data back to the cache
              store.writeQuery({ ...query, data: storedData });
            });
          },
        })
        .then(() => {
          this.$toastSuccess(
            this.$t(
              "lesrooster.timetable_management.snacks.lesson_change_length.success",
            ),
          );
        })
        .catch(() => {
          this.$toastError(
            this.$t(
              "lesrooster.timetable_management.snacks.lesson_change_length.error",
            ),
          );
        });
    },
    prolongLessonBundle(lessonBundle) {
      // Find next slot on the same day
      const slotEnd = this.slots
        .filter(
          (slot) =>
            slot.weekday === lessonBundle.slotEnd.weekday &&
            slot.period > lessonBundle.slotEnd.period,
        )
        .reduce((prev, current) =>
          prev.period < current.period ? prev : current,
        );

      this.changeLessonBundleSlots(
        lessonBundle,
        lessonBundle.slotStart,
        slotEnd,
      );
    },
    shortenLessonBundle(lessonBundle) {
      // Find previous slot on the same day
      const slotEnd = this.slots
        .filter(
          (slot) =>
            slot.weekday === lessonBundle.slotEnd.weekday &&
            slot.period < lessonBundle.slotEnd.period,
        )
        .reduce((prev, current) =>
          prev.period > current.period ? prev : current,
        );

      this.changeLessonBundleSlots(
        lessonBundle,
        lessonBundle.slotStart,
        slotEnd,
      );
    },
    deleteLessonBundle(lessonBundle) {
      this.itemsToDelete = [lessonBundle];
      this.deleteDialog = true;
    },
    teacherClick(teacher) {
      // A teacher was selected for miniplan
      this.selectedObjectType = "teacher";
      this.selectedObject = teacher.id;
      this.selectedObjectTitle = teacher.fullName;
      this.selectedObjectDialogOpen = true;
    },
    roomClick(room) {
      // A room was selected for miniplan
      this.selectedObjectType = "room";
      this.selectedObject = room.id;
      this.selectedObjectTitle = room.name;
      this.selectedObjectDialogOpen = true;
    },
    editLessonClick(lesson) {
      this.lessonEdit.id = lesson.id;
      this.lessonEdit.object = lesson;
      this.lessonEdit.open = true;
    },
    getTeacherList(subjectTeachers) {
      return [
        {
          header: this.$t(
            "lesrooster.timebound_course_config.subject_teachers",
          ),
        },
        ...this.persons.filter((person) =>
          subjectTeachers.find((teacher) => teacher.id === person.id),
        ),
        { divider: true },
        { header: this.$t("lesrooster.timebound_course_config.all_teachers") },
        ...this.persons.filter(
          (person) =>
            !subjectTeachers.find((teacher) => teacher.id === person.id),
        ),
      ];
    },
    handleLessonEditUpdate(store, lesson) {
      const query = {
        ...this.$apollo.queries.lessonBundles.options,
        variables: JSON.parse(
          this.$apollo.queries.lessonBundles.previousVariablesJson,
        ),
      };
      // Read the data from cache for query
      const storedData = store.readQuery(query);

      if (!storedData) {
        // There are no data in the cache yet
        return;
      }

      let lessonIndex = -1;

      const bundleIndex = storedData.lessonBundles.findIndex((lessonBundle) => {
        const index = lessonBundle.lessons.findIndex(
          (lessonObject) => lessonObject.id === lesson.id,
        );

        if (index < 0) {
          return false;
        }

        lessonIndex = index;
        return true;
      });

      if (bundleIndex === -1 || lessonIndex === -1) {
        return;
      }

      storedData.lessonBundles[bundleIndex].lessons[lessonIndex].subject =
        lesson.subject;
      storedData.lessonBundles[bundleIndex].lessons[lessonIndex].teachers =
        lesson.teachers;
      storedData.lessonBundles[bundleIndex].lessons[lessonIndex].rooms =
        lesson.rooms;

      // Write data back to the cache
      store.writeQuery({ ...query, data: storedData });
    },
    handleLessonEditSave() {
      this.$toastSuccess(
        this.$t("lesrooster.timetable_management.snacks.lesson_edit.success"),
      );
    },
    handleLessonEditError() {
      this.$toastError(
        this.$t("lesrooster.timetable_management.snacks.lesson_edit.error"),
      );
    },
    lessonEditGetPatchData(lesson) {
      return {
        id: lesson.id,
        subject: lesson.subject.id,
        teachers: lesson.teachers.map((teacher) => teacher.id),
        rooms: lesson.rooms.map((room) => room.id),
      };
    },
    courseSearchFilter(items, search) {
      if (!search || !items.length) return items;
      search = (search || "").trim().toLowerCase();
      if (!search) return items;

      return items.filter((item) => {
        return (
          item.data.name?.toLowerCase().includes(search) ||
          item.data.subject?.name?.toLowerCase().includes(search) ||
          item.data.subject?.teachers?.some(
            (teacher) =>
              teacher.fullName?.toLowerCase().includes(search) ||
              teacher.shortName?.toLowerCase().includes(search),
          ) ||
          item.data.teachers?.some(
            (teacher) =>
              teacher.fullName?.toLowerCase().includes(search) ||
              teacher.shortName?.toLowerCase().includes(search),
          ) ||
          item.data.groups?.some(
            (group) =>
              group.name?.toLowerCase().includes(search) ||
              group.shortName?.toLowerCase().includes(search),
          )
        );
      });
    },
    formatTimeGrid(item) {
      if (!item) return null;
      if (item.group === null) {
        return this.$t(
          "lesrooster.validity_range.time_grid.repr.generic",
          item.validityRange,
        );
      }
      return this.$t("lesrooster.validity_range.time_grid.repr.default", [
        item.validityRange.name,
        item.group.name,
      ]);
    },
    timeRangesByWeekdays(period) {
      return period.slots
        .map((slot) => ({ timeStart: slot.timeStart, timeEnd: slot.timeEnd }))
        .filter(
          (value, index, self) =>
            index ===
            self.findIndex(
              (timeRange) =>
                timeRange.timeStart === value.timeStart &&
                timeRange.timeEnd === value.timeEnd,
            ),
        )
        .map((timeRange) => ({
          ...timeRange,
          weekdays: period.slots
            .filter(
              (slot) =>
                slot.timeStart === timeRange.timeStart &&
                slot.timeEnd === timeRange.timeEnd,
            )
            .map((slot) => slot.weekday),
        }));
    },
    handleContainerDrag(element, type) {
      if (type === "start") {
        this.draggedItem = element;
      } else {
        this.draggedItem = null;
      }
    },
    setInitialTimeGrid(timeGrids) {
      if (!this.internalTimeGrid?.id) {
        this.internalTimeGrid = timeGrids.find(
          this.$route.params.timeGrid
            ? (timeGrid) => timeGrid.id === this.$route.params.timeGrid
            : (timeGrid) =>
                timeGrid.validityRange.isCurrent &&
                (!timeGrid.group ||
                  timeGrid.group?.id === this.$route.params.group),
        );
      }
    },
  },
});
</script>

<template>
  <div>
    <v-row>
      <v-col cols="12" lg="8" xl="9">
        <div class="d-flex justify-space-between flex-wrap align-center">
          <secondary-action-button
            i18n-key="lesrooster.timetable_management.back"
            :to="{ name: 'cursus.school_structure' }"
          />

          <v-spacer />

          <time-grid-field
            outlined
            filled
            label="Select Validity Range"
            hide-details
            v-model="internalTimeGrid"
            @items="setInitialTimeGrid"
          />

          <v-autocomplete
            outlined
            filled
            hide-details
            label="Select Group"
            :items="groups"
            item-text="name"
            item-value="id"
            return-object
            v-model="selectedGroup"
            :loading="$apollo.queries.groups.loading"
            :disabled="!internalTimeGrid?.id"
            class="mr-4"
          />
        </div>
      </v-col>

      <v-col
        cols="12"
        lg="4"
        xl="3"
        class="d-flex justify-space-between flex-wrap align-center"
      >
        <secondary-action-button
          i18n-key="lesrooster.actions.copy_last_configuration"
          block
          disabled
        />
      </v-col>

      <v-col cols="12" lg="8" xl="9" class="align-self-start" id="grid">
        <div id="weekdays">
          <v-card
            v-for="weekday in weekdays"
            :key="weekday"
            class="d-flex justify-center align-center"
          >
            <v-card-title class="text-body-1">{{
              $t("weekdays." + weekday)
            }}</v-card-title>
          </v-card>
        </div>
        <div id="periods">
          <period-card
            v-for="(period, index) in periods"
            :key="'period-' + period"
            :period="period"
            :weekdays="weekdays"
            :time-ranges="
              timeRangesByWeekdays(
                slotsByPeriods.find(
                  (periodWithSlots) => periodWithSlots.period === period,
                ),
              )
            "
          />
        </div>
        <drag-grid
          :cols="weekdays.length"
          :rows="periods.length"
          :value="gridItems"
          :loading="gridLoading"
          context="timetable"
          :disabled-fields="disabledSlots"
          @itemChanged="itemMovedToLessons"
          grid-id="lessonBundles"
          id="timetable"
          multiple-items-y
          @containerDragStart="handleContainerDrag($event, 'start')"
          @containerDragEnd="handleContainerDrag($event, 'end')"
        >
          <template #item="item">
            <v-menu
              open-on-hover
              offset-y
              :open-on-click="false"
              :rounded="item.data.lessons.length === 1 ? 'pill' : 'xl'"
              bottom
              min-width="max-content"
              nudge-right="40%"
            >
              <template #activator="{ attrs, on }">
                <bundle-card
                  :bundle="item.data"
                  rounded="lg"
                  class="d-flex"
                  v-bind="attrs"
                  v-on="on"
                  :highlighted-rooms="draggedRooms"
                  :highlighted-teachers="draggedTeachers"
                  @click:teacher="teacherClick"
                  @click:room="roomClick"
                />
              </template>

              <v-card
                style="width: max-content"
                class="d-flex flex-column align-center"
              >
                <div>
                  <v-btn
                    icon
                    :disabled="!item.data.canDelete"
                    @click="deleteLessonBundle(item.data)"
                  >
                    <v-icon>$deleteContent</v-icon>
                  </v-btn>
                  <v-btn
                    icon
                    :disabled="!canShortenLessonBundle(item.data)"
                    @click="shortenLessonBundle(item.data)"
                  >
                    <v-icon>mdi-minus</v-icon>
                  </v-btn>
                  <v-btn
                    icon
                    :disabled="!canProlongLessonBundle(item.data)"
                    @click="prolongLessonBundle(item.data)"
                  >
                    <v-icon>mdi-plus</v-icon>
                  </v-btn>
                  <v-btn
                    v-if="item.data.lessons.length === 1"
                    icon
                    @click="editLessonClick(item.data.lessons[0])"
                  >
                    <v-icon>$edit</v-icon>
                  </v-btn>
                </div>
                <template v-if="item.data.lessons.length > 1">
                  <v-list-item
                    v-for="lesson in item.data.lessons"
                    :key="lesson.id"
                    dense
                    @click="editLessonClick(lesson)"
                  >
                    <v-list-item-icon>
                      <v-icon>$edit</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>
                      {{ lesson.subject.name }}
                    </v-list-item-title>
                  </v-list-item>
                </template>
              </v-card>
            </v-menu>
          </template>
          <template #loader>
            <v-skeleton-loader type="sentences" />
          </template>
          <template #highlight>
            <v-skeleton-loader
              type="image"
              boilerplate
              height="100%"
              id="highlight"
            />
          </template>
          <template #disabledField="{ isDraggedOver }">
            <v-fade-transition>
              <blocking-card v-show="isDraggedOver" />
            </v-fade-transition>
          </template>
          <template v-for="overlayBundle in overlayBundles">
            <timetable-overlay-card
              v-if="draggedItem"
              v-show="draggedItem?.data.id !== overlayBundle.id"
              :dragged-item="draggedItem?.data"
              :periods="periods"
              :weekdays="weekdays"
              :bundle="overlayBundle"
              :key="'overlay-' + overlayBundle.id"
            />
          </template>
        </drag-grid>
      </v-col>

      <v-col cols="12" lg="4" xl="3">
        <v-card>
          <v-card-text>
            <v-text-field
              search
              filled
              rounded
              v-model="courseSearch"
              clearable
              :label="$t('lesrooster.actions.search_courses')"
              :hint="totalLessonRatio"
              persistent-hint
            />
            <v-data-iterator
              :items="griddedCourseBundles"
              item-key="key"
              :items-per-page="-1"
              single-expand
              :search="courseSearch"
              sort-by="data.lessonRatio"
              :custom-filter="courseSearchFilter"
            >
              <template #default="{ items }">
                <drag-grid
                  :cols="3"
                  :rows="4"
                  :value="items"
                  :loading="$apollo.queries.courseBundles.loading"
                  no-highlight
                  context="timetable"
                  @itemChanged="itemMovedToCourses"
                  grid-id="courseBundles"
                  @containerDragStart="handleContainerDrag($event, 'start')"
                  @containerDragEnd="handleContainerDrag($event, 'end')"
                >
                  <template #item="item">
                    <bundle-card
                      :bundle="item.data"
                      rounded="lg"
                      :highlighted-rooms="draggedRooms"
                      :highlighted-teachers="draggedTeachers"
                      @click:teacher="teacherClick"
                      @click:room="roomClick"
                    >
                      <lesson-ratio-chip :course="item.data" />
                    </bundle-card>
                  </template>
                  <template #loader>
                    <v-skeleton-loader type="image" />
                  </template>
                </drag-grid>
              </template>
            </v-data-iterator>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <mobile-fullscreen-dialog
      v-model="selectedObjectDialogOpen"
      max-width="75vw"
    >
      <v-card>
        <v-card-title class="justify-space-between">
          <span>
            {{
              $t("lesrooster.timetable_management.timetable_for", {
                name: selectedObjectTitle,
              })
            }}
          </span>

          <v-spacer />

          <v-tabs
            v-model="selectedObjectDialogTab"
            color="secondary"
            right
            v-if="timeGrids && timeGrids.length > 1"
            class="width-max-content"
          >
            <v-tab
              v-for="timeGrid in timeGrids"
              :key="'tabSelector-' + timeGrid.id"
            >
              {{ formatTimeGrid(timeGrid) }}
            </v-tab>
          </v-tabs>
        </v-card-title>
        <v-card-text>
          <v-tabs-items v-model="selectedObjectDialogTab">
            <v-tab-item
              v-for="timeGrid in timeGrids"
              :key="'tabItem-' + timeGrid.id"
            >
              <teacher-time-table
                v-if="internalTimeGrid && selectedObjectType === 'teacher'"
                :id="selectedObject"
                :time-grid="timeGrid"
                class="fill-height"
              />
              <room-time-table
                v-if="internalTimeGrid && selectedObjectType === 'room'"
                :id="selectedObject"
                :time-grid="timeGrid"
                class="fill-height"
              />
            </v-tab-item>
          </v-tabs-items>
        </v-card-text>
      </v-card>
    </mobile-fullscreen-dialog>

    <delete-dialog
      :gql-delete-mutation="deleteMutation"
      :affected-query="$apollo.queries.lessonBundles"
      gql-data-key="lessonBundles"
      v-model="deleteDialog"
      :items="itemsToDelete"
    >
      <template #body>
        <ul class="text-body-1">
          <li v-for="item in itemsToDelete" :key="'delete-' + item.id">
            <span
              v-for="lesson in item.lessons"
              :key="'delete-' + lesson.subject.id"
            >
              {{ lesson.subject.name }}
            </span>
          </li>
        </ul>
      </template>
    </delete-dialog>

    <dialog-object-form
      :is-create="false"
      :default-item="lessonEdit.object"
      :edit-item="lessonEdit.object"
      :fields="lessonEdit.fields"
      v-model="lessonEdit.open"
      item-title-attribute="course.name"
      :gql-patch-mutation="lessonEdit.mutation"
      :get-patch-data="lessonEditGetPatchData"
      @cancel="lessonEdit.open = false"
      @save="handleLessonEditSave"
      @error="handleLessonEditError"
      @update="handleLessonEditUpdate"
      force-model-item-update
    >
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #subject.field="{ attrs, on }">
        <subject-field v-bind="attrs" v-on="on" />
      </template>

      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #teachers.field="{ attrs, on, item }">
        <v-autocomplete
          multiple
          return-object
          :items="getTeacherList(item.subject?.teachers || [])"
          item-text="fullName"
          item-value="id"
          v-bind="attrs"
          v-on="on"
          :loading="$apollo.queries.persons.loading"
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
      </template>

      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #rooms.field="{ attrs, on }">
        <v-autocomplete
          multiple
          return-object
          :items="rooms"
          item-text="name"
          item-value="id"
          :loading="$apollo.queries.rooms.loading"
          v-bind="attrs"
          v-on="on"
        />
      </template>
    </dialog-object-form>
  </div>
</template>

<style>
#highlight > .v-skeleton-loader__image {
  height: 100%;
}
</style>

<style scoped lang="scss">
.big {
  width: 36px;
}

.spacer {
  width: 36px;
}

.width-max-content {
  width: max-content;
}

#grid {
  display: grid;
  grid-template: ". weekdays" auto "periods timetable" auto / min-content auto;
  gap: 0.5rem;
}

#weekdays {
  grid-area: weekdays;
  display: flex;
  flex-direction: row;
  width: 100%;
  justify-content: space-between;
  gap: 0.5rem;

  & > * {
    width: 100%;
  }
}

#periods {
  grid-area: periods;
  display: flex;
  flex-direction: column;
  height: 100%;
  justify-content: space-between;
  gap: 0.5rem;

  & > * {
    height: 100%;
  }
}

#timetable {
  grid-area: timetable;
  gap: 0.5rem;
}
</style>
