<template>
  <ApolloMutation
    v-if="item.status !== 'PUBLISHED'"
    :mutation="publishValidityRange"
    :variables="{ id: item.id }"
    @done="onDone"
    @error="handleMutationError"
    tag="span"
  >
    <template #default="{ mutate, loading, error }">
      <confirm-dialog v-model="confirmDialog" @confirm="mutate()">
        <template #title>
          {{ $t("lesrooster.validity_range.publish.confirm_title", item) }}
        </template>
        <template #text>
          {{
            $t("lesrooster.validity_range.publish.confirm_explanation", item)
          }}
        </template>
        <template #confirm>
          {{ $t("lesrooster.validity_range.publish.confirm_button") }}
        </template>
      </confirm-dialog>
      <secondary-action-button
        icon-text="mdi-publish"
        i18n-key="lesrooster.validity_range.publish.button"
        @click="confirmDialog = true"
        :loading="loading"
      ></secondary-action-button>
    </template>
  </ApolloMutation>
</template>

<script setup>
import SecondaryActionButton from "aleksis.core/components/generic/buttons/SecondaryActionButton.vue";
import ConfirmDialog from "aleksis.core/components/generic/dialogs/ConfirmDialog.vue";
</script>
<script>
import { publishValidityRange } from "./validityRange.graphql";
export default {
  name: "PublishValidityRange",
  data() {
    return {
      confirmDialog: false,
    };
  },
  methods: {
    onDone() {
      this.$activateFrequentCeleryPolling();
    },
  },
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
};
</script>
