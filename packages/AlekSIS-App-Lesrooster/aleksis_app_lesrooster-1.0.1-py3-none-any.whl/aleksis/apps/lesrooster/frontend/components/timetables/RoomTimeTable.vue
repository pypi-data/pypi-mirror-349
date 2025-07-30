<script>
import { defineComponent } from "vue";
import { lessonsRoom } from "./timetables.graphql";
import MiniTimeTable from "./MiniTimeTable.vue";

export default defineComponent({
  name: "RoomTimeTable",
  extends: MiniTimeTable,
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  computed: {
    lessons() {
      return this.lessonsRoom;
    },
    loading() {
      return this.$apollo.queries.lessonsRoom.loading;
    },
  },
  apollo: {
    lessonsRoom: {
      query: lessonsRoom,
      variables() {
        return {
          timeGrid: this.timeGrid.id,
          room: this.id,
        };
      },
      skip() {
        return this.timeGrid === null;
      },
    },
  },
});
</script>
