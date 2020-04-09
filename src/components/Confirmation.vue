<template>
  <div
  v-if="isVisible">
    <b-alert variant="success" show>{{message}}
      <button type="button" id="close-allert" class="btn btn-danger btn-sm"
                @click  ="hideEl">X</button>
                </b-alert>
                </div>
</template>

<script>
export default {
  props: ['message', 'isVisible'],
  data: () => (
    {
      isElVisible: true,
    }
  ),
  methods: {
    hideEl() {
      this.isVisible = false;
    },
  },
};
</script>

<style scoped>
button#close-allert {
  margin-left: 30px;
}
</style>
