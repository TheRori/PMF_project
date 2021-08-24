import Vue from 'vue';
import VueRouter from 'vue-router';
import stream from '../components/stream.vue';
import Index from '../components/index.vue';
import ViewImg from '../components/view_img.vue';
import posImg from '../components/posImg.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'index',
    component: Index,
    alias: '/index',
  },
  {
    path: '/stream/:type/:project/:pos',
    name: 'Stream',
    component: stream,
  },
  {
    path: '/view_pos_img/:project/:pos',
    name: 'Position image',
    component: posImg,
  },
  {
    path: '/view_img/:load',
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
