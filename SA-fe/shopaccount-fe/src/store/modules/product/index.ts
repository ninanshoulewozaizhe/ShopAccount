import { Module } from 'vuex';
import { State } from './typings';
import {
  GET_ALL_PRODUCTS,
  MODIFY_ALL_PRODUCTS,
  LOAD_ALL_PRODUCTS
} from './constants';
import { httpRequestSilence } from '@/utils/httpRequest';
import { IResponse } from '@/typing/vuex/typings';
import { IProductItem } from '@/typing/home/typings';

export default {
  namespaced: true,
  state: () => ({
    allProducts: []
  }),
  actions: {
    async [LOAD_ALL_PRODUCTS]({ commit }): Promise<string> {
      try {
        const { data } = await httpRequestSilence.get<IResponse<IProductItem[]> >(
          `/products`
        );
        if (data.status) {
          commit(MODIFY_ALL_PRODUCTS, data.data);
          return Promise.resolve('OK');
        } else {
          return Promise.resolve(data.message);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    }
  },
  mutations: {
    [MODIFY_ALL_PRODUCTS](state, payload: IProductItem[]) {
      state.allProducts = payload;
    }
  },
  getters: {
    [GET_ALL_PRODUCTS](state): IProductItem[] {
      return state.allProducts;
    }
  }
} as Module<State, any>;
