<script>
import { defineComponent } from "vue";
import { lessonsTeacher } from "./timetables.graphql";
import MiniTimeTable from "./MiniTimeTable.vue";

export default defineComponent({
  name: "TeacherTimeTable",
  extends: MiniTimeTable,
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  computed: {
    lessons() {
      return this.lessonsTeacher;
    },
    loading() {
      return this.$apollo.queries.lessonsTeacher.loading;
    },
  },
  apollo: {
    lessonsTeacher: {
      query: lessonsTeacher,
      variables() {
        return {
          timeGrid: this.timeGrid.id,
          teacher: this.id,
        };
      },
      skip() {
        return this.timeGrid === null;
      },
    },
  },
});
</script>
