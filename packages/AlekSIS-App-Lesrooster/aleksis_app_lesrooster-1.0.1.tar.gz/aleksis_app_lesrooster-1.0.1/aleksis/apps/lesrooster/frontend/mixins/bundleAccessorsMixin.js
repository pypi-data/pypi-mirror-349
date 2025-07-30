/**
 * This mixin provides accessors for course*lesson bundles
 */
export default {
  methods: {
    /**
     * Removes duplicate objects from an array based on their `id` property.
     *
     * @param {Array<{id: string|number, [key: string]: any}>} array - An array of objects, each having an `id` property and possibly other attributes.
     * @return {Array<{id: string|number, [key: string]: any}>} - A new array with duplicates removed.
     */
    removeDuplicatesById(array) {
      return array.filter(
        (value, index, self) =>
          index ===
          self.findIndex(
            (t) => t.place === value.place && t.name === value.name,
          ),
      );
    },
    bundleChildren(bundle) {
      return bundle.courses || bundle.lessons;
    },
    bundleSubjects(bundle) {
      const subjects = this.bundleChildren(bundle).flatMap(
        (child) => child.subject,
      );
      return this.removeDuplicatesById(subjects);
    },
    bundleTeachers(bundle) {
      const teachers = this.bundleChildren(bundle).flatMap(
        (child) => child.teachers,
      );
      return this.removeDuplicatesById(teachers);
    },
    bundleRooms(bundle) {
      const rooms = bundle.courses
        ? bundle.courses.map((course) => course.defaultRoom)
        : bundle.lessons.flatMap((lesson) => lesson.rooms);
      return this.removeDuplicatesById(rooms.filter((room) => room));
    },
  },
};
