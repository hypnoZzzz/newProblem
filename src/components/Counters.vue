<template>
    <div>
        <h4>Всего задач: {{counterMessage}} </h4>
        <h4>Выполнено: {{completedTasks}} </h4>
        <h4>Не выполнено: {{outstandingTasks}} </h4>
    </div>
</template>
<script>
export default {
  props: ['counterMessage', 'completedTasks', 'outstandingTasks'],
};
</script>
<style scoped>
.counter {
    text-align: left;
}
</style>
