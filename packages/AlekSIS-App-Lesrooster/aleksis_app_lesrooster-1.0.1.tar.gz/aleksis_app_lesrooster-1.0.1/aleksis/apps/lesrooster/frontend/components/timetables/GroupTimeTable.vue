<script>
import { defineComponent } from "vue";
import { lessonsGroup } from "./timetables.graphql";
import MiniTimeTable from "./MiniTimeTable.vue";

export default defineComponent({
  name: "GroupTimeTable",
  extends: MiniTimeTable,
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  computed: {
    lessons() {
      return this.lessonsGroup;
    },
    loading() {
      return this.$apollo.queries.lessonsGroup.loading;
    },
  },
  apollo: {
    lessonsGroup: {
      query: lessonsGroup,
      variables() {
        return {
          timeGrid: this.timeGrid.id,
          group: this.id,
        };
      },
      skip() {
        return this.timeGrid === null;
      },
    },
  },
});
</script>
