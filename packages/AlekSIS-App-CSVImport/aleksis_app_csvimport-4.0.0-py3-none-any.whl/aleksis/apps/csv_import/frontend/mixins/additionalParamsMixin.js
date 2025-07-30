/**
 * This mixin provides shared props for additional params rows in import view.
 */
export default {
  props: {
    /**
     * The current additional params
     */
    additionalParams: {
      type: Object,
      required: true,
    },
  },
};
