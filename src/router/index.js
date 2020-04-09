import Vue from 'vue';
import VueRouter from 'vue-router';
//  import Fetch from '@/components/Fetch.vue';
import Todos from '@/components/Todos.vue';

Vue.use(VueRouter);
const routes = [
  {
    path: '/todos',
    name: 'todos',
    component: Todos,
  },
];
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});
export default router;
