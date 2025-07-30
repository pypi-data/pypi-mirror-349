<script>
import additionalParamsMixin from "aleksis.apps.csv_import/mixins/additionalParamsMixin.js";
import { validityRangeById } from "./additionalParams.graphql";

export default {
  name: "CSVAdditionalParams",
  mixins: [additionalParamsMixin],
  apollo: {
    validityRange: {
      query: validityRangeById,
      variables() {
        return { id: this.additionalParams?.validity_range };
      },
      skip() {
        return !this.additionalParams.validity_range;
      },
    },
  },
};
</script>
<template>
  <div class="mb-2">
    <span v-if="additionalParams.validity_range">
      {{
        $t("lesrooster.validity_range.import_data_param", {
          name: validityRange?.name || additionalParams.validity_range,
        })
      }}
    </span>
  </div>
</template>
