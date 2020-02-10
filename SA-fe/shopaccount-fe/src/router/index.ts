import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import BasicLayout from '../views/BasicLayout.vue';
Vue.use(VueRouter);

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/login/Login.vue')
  },
  {
    path: '/',
    component: BasicLayout,
    children: [
      {
        path: '',
        redirect: '/home'
      },
      {
        path: 'home',
        name: 'home',
        component: () => import('../views/home/Home.vue')
      },
      {
        path: 'shops',
        name: 'shops',
        component: () => import('../views/shops/Shops.vue')
      },
      {
        path: 'salesStatus',
        name: 'salesStatus',
        component: () => import('../views/salesStatus/SalesStatus.vue')
      }
    ]
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router;
