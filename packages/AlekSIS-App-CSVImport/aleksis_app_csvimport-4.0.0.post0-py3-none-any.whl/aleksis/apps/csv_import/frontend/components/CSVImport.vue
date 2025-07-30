<script setup>
import SchoolTermField from "aleksis.core/components/school_term/SchoolTermField.vue";
import ImportTemplateField from "./ImportTemplateField.vue";
import FileField from "aleksis.core/components/generic/forms/FileField.vue";
import CeleryProgressInner from "aleksis.core/components/celery_progress/CeleryProgressInner.vue";
</script>
<script>
import formRulesMixin from "aleksis.core/mixins/formRulesMixin.js";
import mutateMixin from "aleksis.core/mixins/mutateMixin.js";
import { csvImport } from "./import.graphql";
import { collections } from "aleksisAppImporter";

export default {
  name: "CSVImport",
  mixins: [formRulesMixin, mutateMixin],
  data() {
    return {
      step: 1,
      valid: false,
      importData: {
        csv: null,
        schoolTerm: null,
        template: null,
        create: true,
        additionalParams: {},
      },
      taskId: null,
      csvAdditionalParams: collections.csv_importAdditionalParams.items,
    };
  },
  mounted() {
    this.importData.additionalParams = this.$route.query || {};
  },
  methods: {
    doImport() {
      this.handleLoading(true);

      this.$apollo
        .mutate({
          mutation: csvImport,
          variables: {
            input: {
              ...this.importData,
              additionalParams: JSON.stringify(
                this.importData.additionalParams,
              ),
            },
          },
        })
        .then(({ data }) => {
          console.log(data);
          this.taskId = data.csvImport.taskId;
          this.step = 2;
        })
        .catch((error) => {
          this.handleMutationError(error);
        })
        .finally(() => {
          this.handleLoading(false);
        });
    },
  },
};
</script>

<template>
  <v-stepper v-model="step" class="mb-4">
    <v-stepper-header>
      <v-stepper-step :complete="step >= 1" :step="1">
        {{ $t("csv.import.prepare_title") }}
      </v-stepper-step>
      <v-divider></v-divider>
      <v-stepper-step :complete="step >= 2" :step="2">
        {{ $t("csv.import.do_import_title") }}
      </v-stepper-step>
    </v-stepper-header>
    <v-stepper-items>
      <v-stepper-content step="1">
        <message-box type="info">
          {{ $t("csv.import.instructions") }}
        </message-box>
        <v-form v-model="valid">
          <component
            :is="param.component"
            v-for="(param, idx) in csvAdditionalParams"
            :key="idx"
            :additional-params="importData.additionalParams"
          />
          <file-field
            accept="text/csv,text/plain"
            filled
            :label="$t('csv.import.csv_file')"
            aria-required="true"
            required
            :rules="$rules().required.build()"
            v-model="importData.csv"
          />
          <import-template-field
            filled
            :label="$t('csv.import.import_template')"
            aria-required="true"
            required
            :rules="$rules().required.build()"
            v-model="importData.template"
          />
          <school-term-field
            filled
            :label="$t('csv.import.school_term')"
            aria-required="true"
            required
            :rules="$rules().required.build()"
            v-model="importData.schoolTerm"
          />
          <v-switch
            class="ml-1"
            v-model="importData.create"
            inset
            :false-value="false"
            :true-value="true"
            :label="$t('csv.import.create_new_objects')"
          />
        </v-form>
        <div class="d-flex">
          <v-spacer />
          <primary-action-button
            i18n-key="csv.import.import_data"
            :disabled="!valid"
            :loading="loading"
            @click="doImport"
          />
        </div>
      </v-stepper-content>
      <v-stepper-content step="2">
        <celery-progress-inner v-if="taskId" :task-id="taskId" />
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
</template>

<style scoped></style>
