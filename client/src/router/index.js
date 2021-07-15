import Vue from 'vue';
import VueRouter from 'vue-router';
import stream from '../components/stream.vue';
import Index from '../components/index.vue';
import ViewImg from '../components/view_img.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'index',
    component: Index,
    alias: '/index',
  },
  {
    path: '/stream',
    name: 'Stream',
    component: stream,
  },
  {
    path: '/view_img',
    name: 'View_Img',
    component: ViewImg,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
