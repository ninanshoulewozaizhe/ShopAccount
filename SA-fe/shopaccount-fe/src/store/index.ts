import Vue from 'vue';
import Vuex from 'vuex';
import user from './modules/user';
import shop from './modules/shop';
import product from './modules/product';
import salesStatus from './modules/salesStatus';
import { ModuleState } from '@/typing/vuex/typings';

Vue.use(Vuex);

const modules = {
  user,
  shop,
  product,
  salesStatus
};

const rootStore = new Vuex.Store<RootState>({
  modules,
  // plugins: [enhanceWithLoadingModule],
  strict: process.env.NODE_ENV !== 'production'
});

export type RootStore = typeof rootStore;

export type RootState = {
  [P in keyof typeof modules]: ModuleState<(typeof modules)[P]>
};

export default rootStore;
