import Vue from 'vue';
import Vuex from 'vuex';
import { ModuleState } from '@/typing/vuex/typings';

Vue.use(Vuex);

const modules = {};

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
