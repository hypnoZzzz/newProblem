<template>
  <div class="container">
    <div class="col-sm-10">
      <h1>Задачи</h1>
        <counters class="counter" :counterMessage = "counterMessage"
        :completedTasks = "completedTasks" :outstandingTasks = "outstandingTasks"></counters>
       <confirmation :message="message" :isVisible=true v-if="showConfirmation"></confirmation>
      <button type="button" id="task-add" class="btn btn-success btn-sm align-left d-block"
      v-b-modal.todo-modal>
          Добавить задачу
          </button>

      <table class="table table-dark table-stripped table-hover">
        <thead class="thead-light">
          <tr>
            <th>Uid</th>
            <th>Описание</th>
            <th>Статус</th>
            <th></th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="(todo, index) in todos" :key="index">
            <td class="todo-uid">{{ todo.uid }}</td>
            <td>{{ todo.description }}</td>
            <td>
              <span v-if="todo.is_completed">Выполнено</span>
              <span v-else>Не выполнено</span>
            </td>
            <td>
              <div class="btn-group" role="group">
                <button type="button"
        class="btn btn-secondary btn-sm"
        v-b-modal.todo-update-modal
        @click="updateTodo(todo)"
        >
    Обновить
</button>
                &nbsp;
                <button type="button" class="btn btn-danger btn-sm"
                @click="deleteTodo(todo)">X</button>
              </div>
            </td>
          </tr>
        </tbody>

      </table>
    <b-modal ref="addTodoModal"
         id="todo-modal"
         title="Добавить задачу"
         hide-footer>
  <b-form @submit="onSubmit" @reset="onReset" class="w-100">
  <b-form-group id="form-description-group"
                label="Описание:"
                label-for="form-description-input">
    <b-form-input id="form-description-input"
                  type="text"
                  v-model="addTodoForm.description"
                  required
                  placeholder="Завести задачу">
    </b-form-input>
  </b-form-group>
  <b-form-group id="form-complete-group">
    <b-form-checkbox-group v-model="addTodoForm.is_completed" id="form-checks">
      <b-form-checkbox value="true">Задача выполнена?</b-form-checkbox>
    </b-form-checkbox-group>
    </b-form-group>
    <b-button type="submit" variant="primary">Добавить</b-button>
    <b-button type="reset" variant="danger">Сброс</b-button>
  </b-form>
</b-modal>
    </div>
      <!-- вынести в отдельное -->
    <b-modal ref="updateTodoModal"
         id="todo-update-modal"
         title="Update"
         hide-footer>
  <b-form @submit="onUpdateSubmit" @reset="onUpdateReset" class="w-100">
  <b-form-group id="form-update-description-group"
                label="Описание:"
                label-for="form-update-description-input">
    <b-form-input id="form-update-description-input"
                  type="text"
                  v-model="updateTodoForm.description"
                  required>
    </b-form-input>
  </b-form-group>
  <b-form-group id="form-update-complete-group">
    <b-form-checkbox-group v-model="updateTodoForm.is_completed" id="form-update-checks">
      <b-form-checkbox value="true">Задача выполнена?</b-form-checkbox>
    </b-form-checkbox-group>
  </b-form-group>
  <b-button-group>
    <b-button type="submit" variant="primary">Обновить</b-button>
    <b-button type="reset" variant="danger">Сброс</b-button>
  </b-button-group>
  </b-form>
</b-modal>
  </div>
</template>
<script>
import axios from 'axios';
import Confirmation from './Confirmation.vue';
import Counters from './Counters.vue';

const dataURL = 'http://localhost:8081/api/tasks/';

export default {
  name: 'Todos',
  data() {
    return {
      todos: [],
      connection: true,
      addTodoForm: {
        description: '',
        is_completed: [],
      },
      updateTodoForm: {
        uid: 0,
        description: '',
        is_completed: [],
      },
      message: '',
      counterMessage: '',
      completedTasks: '',
      outstandingTasks: '',
      showConfirmation: false,
    };
  },
  methods: {
    getTodos() {
      axios.get(dataURL, {
        validateStatus: (status) => status < 300,
        // остановить запрос, только если код больше или равен 300
      })
        .then((response) => {
          this.todos = response.data.tasks;
          const isTrue = this.todos.filter((item) => item.is_completed === 'true');
          this.counterMessage = this.todos.length;
          this.completedTasks = isTrue.length;
          this.outstandingTasks = (this.counterMessage) - (this.completedTasks);
        })
        .catch((error) => {
          this.message = 'Что-то пошло не так...';
          if (error.response) {
            // Запрос выполнен, и сервер отправил Вам статус код
            // код выпададет из диапазона 2хх (ошибка)
            console.log(error.response.data);
            console.log('Статус ошибки: ', error.response.status);
            console.log(error.response.headers);
          } else if (error.request) {
            // Запрос был сделан, но ответ не получен
            // `error.request` - экземпляр XMLHttpRequest в браузере,
            // http.ClientRequest экземпляр в node.js
            console.error('Ошибка! Сервер не найден!', error.request);
          } else {
          // Что-то пошло не так, вернулась ошибка
            console.error('Error', error.message);
          }
          console.error(error.config);
        });
    },
    resetForm() {
      this.addTodoForm.description = '';
      this.addTodoForm.is_completed = [];
      this.updateTodoForm.description = '';
      this.updateTodoForm.is_completed = [];
    },
    onSubmit(event) {
      event.preventDefault();
      this.$refs.addTodoModal.hide();
      const requestData = {
        description: this.addTodoForm.description,
        is_completed: this.addTodoForm.is_completed[0],
      };
      axios.post(dataURL, requestData)
        .then(() => {
          this.getTodos();
          this.message = `Задача "${requestData.description}" добавлена`;
          this.showConfirmation = true;
        });
      this.resetForm();
    },
    onReset(event) {
      event.preventDefault();
      this.$refs.addTodoModal.hide();
      this.resetForm();
    },
    updateTodo(todo) {
      this.updateTodoForm = todo;
    },
    onUpdateSubmit(event) {
      event.preventDefault();
      this.$refs.updateTodoModal.hide();
      const requestData = {
        description: this.updateTodoForm.description,
        is_completed: this.updateTodoForm.is_completed[0],
      };
      const todoUrl = dataURL + this.updateTodoForm.uid;
      axios.put(todoUrl, requestData)
        .then(() => {
          this.getTodos();
          this.message = `Задача "${requestData.description}" обновлена`;
          this.showConfirmation = true;
        });
    },
    onUpdateReset(event) {
      event.preventDefault();
      this.$refs.updateTodoModal.hide();
      this.resetForm();
    },
    deleteTodo(todo) {
      const todoURL = dataURL + todo.uid;
      axios.delete(todoURL)
        .then(() => {
          this.getTodos();
          this.message = 'Задача удалена из списка';
          this.showConfirmation = true;
        });
    },
  },
  components: {
    confirmation: Confirmation,
    counters: Counters,
  },
  created() {
    this.getTodos();
  },
};
</script>

<style>
button#task-add {
  margin-top: 20px;
  margin-bottom: 20px;
}
h1, td {
  text-align: left;
}
.todo-uid {
  text-align: right;
}
</style>
