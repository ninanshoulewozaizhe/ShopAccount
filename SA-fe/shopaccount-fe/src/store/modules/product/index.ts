import { Module } from 'vuex';
import { State } from './typings';
import {
  GET_ALL_PRODUCTS,
  GET_CUR_SHOP_PRODUCTS,
  MODIFY_ALL_PRODUCTS,
  MODIFY_CUR_SHOP_PRODUCTS,
  LOAD_ALL_PRODUCTS,
  LOAD_CUR_SHOP_PRODUCTS,
  LOAD_CUR_SHOP_PRE_PRODUCTS
} from './constants';
import { httpRequestSilence } from '@/utils/httpRequest';
import { IResponse } from '@/typing/vuex/typings';
import { IProductDetailItem } from '@/typing/productDetail/typings';

export default {
  namespaced: true,
  state: () => ({
    allProducts: [],
    curShopProducts: []
  }),
  actions: {
    async [LOAD_ALL_PRODUCTS]({ commit }): Promise<string> {
      try {
        const { data } = await httpRequestSilence.get<IResponse<IProductDetailItem[]> >(
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
    },
    async [LOAD_CUR_SHOP_PRODUCTS]({ commit }, payload: number): Promise<string> {
      try {
        const { data } = await httpRequestSilence.get<IResponse<IProductDetailItem[]> >(
          `/products/${payload}`
        );
        if (data.status) {
          commit(MODIFY_CUR_SHOP_PRODUCTS, data.data);
          return Promise.resolve('OK');
        } else {
          return Promise.resolve(data.message);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [LOAD_CUR_SHOP_PRE_PRODUCTS]({ commit }, payload: number): Promise<string> {
      try {
        const { data } = await httpRequestSilence.get<IResponse<IProductDetailItem[]> >(
          `/shopPreProducts/${payload}`
        );
        if (data.status) {
          commit(MODIFY_CUR_SHOP_PRODUCTS, data.data);
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
    [MODIFY_ALL_PRODUCTS](state, payload: IProductDetailItem[]) {
      state.allProducts = payload;
    },
    [MODIFY_CUR_SHOP_PRODUCTS](state, payload: IProductDetailItem[]) {
      state.curShopProducts = payload;
    }
  },
  getters: {
    [GET_ALL_PRODUCTS](state): IProductDetailItem[] {
      return state.allProducts;
    },
    [GET_CUR_SHOP_PRODUCTS](state): IProductDetailItem[] {
      return state.curShopProducts;
    }
  }
} as Module<State, any>;
