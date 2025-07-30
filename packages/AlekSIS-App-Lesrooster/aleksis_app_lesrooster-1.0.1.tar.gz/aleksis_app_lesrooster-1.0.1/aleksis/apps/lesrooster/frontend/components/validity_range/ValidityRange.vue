<script setup>
import CRUDList from "aleksis.core/components/generic/CRUDList.vue";
import DateField from "aleksis.core/components/generic/forms/DateField.vue";
import TimeGridChip from "./TimeGridChip.vue";
import MessageBox from "aleksis.core/components/generic/MessageBox.vue";
import CreateButton from "aleksis.core/components/generic/buttons/CreateButton.vue";
import DialogObjectForm from "aleksis.core/components/generic/dialogs/DialogObjectForm.vue";
import DeleteDialog from "aleksis.core/components/generic/dialogs/DeleteDialog.vue";
import ValidityRangeStatusField from "./ValidityRangeStatusField.vue";
import ValidityRangeStatusChip from "./ValidityRangeStatusChip.vue";
import PublishValidityRange from "./PublishValidityRange.vue";
</script>

<template>
  <div>
    <c-r-u-d-list
      :headers="headers"
      :i18n-key="i18nKey"
      create-item-i18n-key="lesrooster.validity_range.create_validity_range"
      :gql-query="gqlQuery"
      :gql-create-mutation="gqlCreateMutation"
      :gql-patch-mutation="gqlPatchMutation"
      :gql-delete-mutation="gqlDeleteMutation"
      :default-item="defaultItem"
      :get-create-data="getCreateData"
      :get-patch-data="getPatchData"
      :enable-filter="true"
      show-expand
      :enable-edit="true"
      ref="crudList"
    >
      <template #status="{ item }">
        <validity-range-status-chip :value="item.status" />
      </template>

      <template #dateStart="{ item }">
        {{ $d(new Date(item.dateStart), "short") }}
      </template>
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #dateStart.field="{ attrs, on, item }">
        <div aria-required="true">
          <date-field
            v-bind="attrs"
            v-on="on"
            :rules="required"
            :max="item ? item.dateEnd : undefined"
            required
          ></date-field>
        </div>
      </template>

      <template #dateEnd="{ item }">
        {{ $d(new Date(item.dateEnd), "short") }}
      </template>
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #dateEnd.field="{ attrs, on, item }">
        <div aria-required="true">
          <date-field
            v-bind="attrs"
            v-on="on"
            required
            :rules="required"
            :min="item ? item.dateStart : undefined"
          ></date-field>
        </div>
      </template>

      <template #filters="{ attrs, on }">
        <validity-range-status-field
          v-bind="attrs('status__iexact')"
          v-on="on('status__iexact')"
          :label="$t('lesrooster.validity_range.status_label')"
        />

        <date-field
          v-bind="attrs('date_end__gte')"
          v-on="on('date_end__gte')"
          :label="$t('school_term.after')"
        />

        <date-field
          v-bind="attrs('date_start__lte')"
          v-on="on('date_start__lte')"
          :label="$t('school_term.before')"
        />
      </template>

      <template #actions="{ item }">
        <!-- FIXME Vue 3: use hasRoute -->
        <secondary-action-button
          v-if="
            $router.resolve({ name: 'csv.csvImport' }).route.matched.length > 0
          "
          icon-text="mdi-table-arrow-left"
          i18n-key="lesrooster.validity_range.import_data"
          :to="{ name: 'csv.csvImport', query: { validity_range: item.id } }"
          class="mr-2"
        ></secondary-action-button>
        <publish-validity-range :item="item" />
      </template>

      <template #expanded-item="{ item }">
        <v-sheet class="my-4">
          <message-box type="error" v-if="item.timeGrids.length === 0">
            {{
              $t(
                "lesrooster.validity_range.time_grid.explanations.none_created",
              )
            }}
          </message-box>
          <message-box
            type="info"
            v-else-if="item.timeGrids.length === 1 && !item.timeGrids[0].group"
          >
            {{
              $t(
                "lesrooster.validity_range.time_grid.explanations.only_generic",
              )
            }}
          </message-box>
          <message-box type="info" v-else-if="item.timeGrids.length === 1">
            {{
              $t(
                "lesrooster.validity_range.time_grid.explanations.only_one_group",
              )
            }}
          </message-box>
          <message-box type="info" v-else>
            {{
              $t(
                "lesrooster.validity_range.time_grid.explanations.multiple_set",
              )
            }}
          </message-box>

          <v-slide-x-transition group>
            <time-grid-chip
              :value="timeGrid"
              v-for="timeGrid in item.timeGrids"
              :key="timeGrid.id"
              @click:close="handleDeleteTimeGridClick(timeGrid, item)"
              class="me-2"
            />
          </v-slide-x-transition>

          <create-button
            i18n-key="lesrooster.validity_range.time_grid.create"
            @click="createTimeGridFor(item)"
          />
        </v-sheet>
      </template>
    </c-r-u-d-list>

    <dialog-object-form
      is-create
      :default-item="timeGrids.object"
      :fields="timeGrids.fields"
      v-model="timeGrids.open"
      item-title-attribute="course.name"
      :get-create-data="timeGrids.getCreateDataBuilder(timeGrids.range)"
      :gql-create-mutation="timeGrids.mutation"
      @cancel="timeGrids.open = false"
      @save="handleTimeGridSave"
      @error="handleTimeGridError"
      @update="handleTimeGridUpdate"
    >
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #isGeneric.field="{ attrs, on }">
        <v-switch
          v-bind="attrs"
          v-on="on"
          :disabled="!genericPossible"
        ></v-switch>
      </template>

      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #group.field="{ attrs, on, item }">
        <v-autocomplete
          :items="selectableGroups"
          item-text="name"
          item-value="id"
          v-bind="attrs"
          v-on="on"
          :disabled="item.isGeneric"
          :loading="$apollo.queries.groups.loading"
        />
      </template>
    </dialog-object-form>

    <delete-dialog
      v-model="timeGrids.deleteOpen"
      :item="timeGrids.deleteItem"
      :gql-mutation="timeGrids.deleteMutation"
      @update="updateTimeGridDelete"
    >
      <template #body>
        {{ $t("lesrooster.validity_range.time_grid.confirm_delete_body") }}
      </template>
    </delete-dialog>
  </div>
</template>

<script>
import {
  validityRanges,
  createValidityRanges,
  deleteValidityRanges,
  updateValidityRanges,
  createTimeGrids,
  deleteTimeGrids,
} from "./validityRange.graphql";
import { gqlGroups } from "../helper.graphql";

export default {
  name: "ValidityRange",
  apollo: {
    groups: {
      query: gqlGroups,
    },
  },
  data() {
    return {
      headers: [
        {
          text: this.$t("lesrooster.validity_range.name"),
          value: "name",
        },
        {
          text: this.$t("lesrooster.validity_range.status_label"),
          value: "status",
          disableEdit: true,
        },
        {
          text: this.$t("lesrooster.validity_range.date_start"),
          value: "dateStart",
        },
        {
          text: this.$t("lesrooster.validity_range.date_end"),
          value: "dateEnd",
        },
      ],
      i18nKey: "lesrooster.validity_range",
      gqlQuery: validityRanges,
      gqlCreateMutation: createValidityRanges,
      gqlPatchMutation: updateValidityRanges,
      gqlDeleteMutation: deleteValidityRanges,
      defaultItem: {
        name: "",
        dateStart: "",
        dateEnd: "",
      },
      required: [(value) => !!value || this.$t("forms.errors.required")],
      timeGrids: {
        open: false,
        deleteOpen: false,
        deleteItem: null,
        deleteMutation: deleteTimeGrids,
        range: null,
        object: {
          isGeneric: false,
          group: null,
        },
        mutation: createTimeGrids,
        fields: [
          {
            text: this.$t(
              "lesrooster.validity_range.time_grid.fields.is_generic",
            ),
            value: "isGeneric",
          },
          {
            text: this.$t("lesrooster.validity_range.time_grid.fields.group"),
            value: "group",
          },
        ],
        getCreateDataBuilder(validityRange) {
          return (model) => ({
            group: model.isGeneric ? null : model.group,
            validityRange: validityRange.id,
          });
        },
      },
    };
  },
  computed: {
    selectableGroups() {
      return this.groups?.filter(
        (group) =>
          !this.timeGrids.range?.timeGrids
            .map((timeGrid) => timeGrid.group?.id)
            .includes(group.id),
      );
    },
    genericPossible() {
      return !this.timeGrids.range.timeGrids.some(
        (timeGrid) => timeGrid.group === null,
      );
    },
  },
  methods: {
    getPatchData(item) {
      item = {
        id: item.id,
        name: item.name,
        dateStart: item.dateStart,
        dateEnd: item.dateEnd,
      };
      return Object.fromEntries(
        Object.entries(item).filter(([key, value]) => value !== undefined),
      );
    },
    createTimeGridFor(validityRange) {
      this.timeGrids.range = validityRange;
      this.timeGrids.open = true;
    },
    handleTimeGridSave() {
      this.$toastSuccess();
    },
    handleTimeGridError() {
      this.$toastError();
    },
    handleTimeGridUpdate(store, timeGrid) {
      const query = {
        ...this.$refs.crudList.$apollo.queries.items.options,
        variables: JSON.parse(
          this.$refs.crudList.$apollo.queries.items.previousVariablesJson,
        ),
      };
      // Read the data from cache for query
      const storedData = store.readQuery(query);

      if (!storedData) {
        // There are no data in the cache yet
        return;
      }

      const index = storedData.items.findIndex(
        (validityRange) => validityRange.id === timeGrid.validityRange.id,
      );
      storedData.items[index].timeGrids.push(timeGrid);

      // Write data back to the cache
      store.writeQuery({ ...query, data: storedData });
    },
    handleDeleteTimeGridClick(timeGrid, validityRange) {
      this.timeGrids.deleteItem = timeGrid;
      this.timeGrids.range = validityRange;
      this.timeGrids.deleteOpen = true;
    },
    updateTimeGridDelete(store) {
      const query = {
        ...this.$refs.crudList.$apollo.queries.items.options,
        variables: JSON.parse(
          this.$refs.crudList.$apollo.queries.items.previousVariablesJson,
        ),
      };
      // Read the data from cache for query
      const storedData = store.readQuery(query);

      if (!storedData) {
        // There are no data in the cache yet
        return;
      }

      const vrIndex = storedData.items.findIndex(
        (validityRange) => validityRange.id === this.timeGrids.range.id,
      );

      // Remove item from stored data
      const tgIndex = storedData.items[vrIndex].timeGrids.findIndex(
        (m) => m.id === this.timeGrids.deleteItem.id,
      );
      storedData.items[vrIndex].timeGrids.splice(tgIndex, 1);

      // Write data back to the cache
      store.writeQuery({ ...query, data: storedData });
    },
  },
};
</script>

<style scoped></style>
