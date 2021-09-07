import Vue from 'vue';
import VueRouter from 'vue-router';
import createScenario from '../components/create_scenario.vue';
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
    path: '/scenario/:load',
    name: 'Create_Scenario',
    component: createScenario,
  },
  {
    path: '/stream/:type/:project/:step/:pos',
    name: 'Stream',
    component: stream,
  },
  {
    path: '/view_pos_img/:project/:pos',
    name: 'Position image',
    component: posImg,
  },
  {
    path: '/view_img/:load/:mode',
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
