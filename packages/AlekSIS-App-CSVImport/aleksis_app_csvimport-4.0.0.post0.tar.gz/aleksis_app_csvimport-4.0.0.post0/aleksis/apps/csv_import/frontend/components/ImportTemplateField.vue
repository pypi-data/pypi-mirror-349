<template>
  <v-autocomplete
    v-bind="$attrs"
    v-on="$listeners"
    hide-no-data
    :items="items"
    item-text="verboseName"
    item-value="id"
    :loading="loading"
  />
</template>

<script>
import queryMixin from "aleksis.core/mixins/queryMixin.js";
import { importTemplates } from "./importTemplates.graphql";

export default {
  name: "ImportTemplateField",
  extends: "v-autocomplete",
  mixins: [queryMixin],
  props: {
    /**
     * The graphQL query used to retrieve the groups.
     */
    gqlQuery: {
      type: Object,
      required: false,
      default: () => importTemplates,
    },
  },
};
</script>
