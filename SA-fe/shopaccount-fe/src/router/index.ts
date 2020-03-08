import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import BasicLayout from '../views/BasicLayout.vue';
import store from '@/store';
import user from '@/store/modules/user';
import { IS_LOGIN, LOAD_USER_PROFILE } from '@/store/modules/user/constants';
Vue.use(VueRouter);

const routes = [
  {
    path: '/login',
    name: 'login',
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
      },
      {
        path: 'shop/:sid',
        name: 'shop-detail',
        component: () => import('../views/shopDetail/ShopDetail.vue')
      },
      {
        path: 'shopManage/:sid',
        name: 'shop-manage',
        component: () => import('../views/shopDetail/ShopManage.vue')
      },
      {
        path: 'product/:pid',
        name: 'product-detail',
        component: () => import('../views/productDetail/ProductDetail.vue')
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

router.beforeEach(async (to, from, next) => {
  // 验证登录态
  const status = await checkUserLogin();
  if (to.path === '/login') {
    if (status) {
      next({ path: '/home' });
    } else {
      next();
    }
  } else {
    if (status) {
      next();
    } else {
      next({ path: '/login' });
    }
  }
});

async function checkUserLogin() {
  if (store.getters[`user/${IS_LOGIN}`]) {
    return Promise.resolve(true);
  } else {
    await store.dispatch(`user/${LOAD_USER_PROFILE}`);
    if (store.getters[`user/${IS_LOGIN}`]) {
      return Promise.resolve(true);
    }
    return Promise.resolve(false);
  }
}

export default router;
