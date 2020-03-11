import { Module } from 'vuex';
import { State } from './typings';
import {
  GET_ALL_PRODUCTS,
  GET_CUR_SHOP_PRODUCTS,
  GET_CUR_PRODUCT,
  MODIFY_ALL_PRODUCTS,
  MODIFY_CUR_SHOP_PRODUCTS,
  MODIFY_CUR_PRODUCT,
  LOAD_ALL_PRODUCTS,
  LOAD_CUR_SHOP_PRODUCTS,
  LOAD_CUR_SHOP_PRE_PRODUCTS,
  LOAD_CUR_PRODUCT,
  ADD_NEW_PRODUCT,
  UPDATE_PRODUCT,
  DELETE_PRODUCT
} from './constants';
import { httpRequestSilence } from '@/utils/httpRequest';
import { IResponse } from '@/typing/vuex/typings';
import { IProductDetailItem } from '@/typing/productDetail/typings';

export default {
  namespaced: true,
  state: () => ({
    allProducts: [],
    curShopProducts: [],
    curProduct: null
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
    },
    async [LOAD_CUR_PRODUCT]({ commit }, payload: number): Promise<string> {
      try {
        const { data } = await httpRequestSilence.get<IResponse<IProductDetailItem> >(
          `/product/${payload}`
        );
        if (data.status) {
          commit(MODIFY_CUR_PRODUCT, data.data);
          return Promise.resolve('OK');
        } else {
          return Promise.resolve(data.message);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [ADD_NEW_PRODUCT]({ commit }, payload: IProductDetailItem): Promise<any> {
      try {
        const { data } = await httpRequestSilence.post<IResponse<any> >(
          `/createProduct`, payload);
        if (data.status) {
          return Promise.resolve({status: true, pid: data.data.pid});
        } else {
          return Promise.resolve(data.message);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [UPDATE_PRODUCT]({ commit }, payload: IProductDetailItem): Promise<string> {
      try {
        const { data } = await httpRequestSilence.put<IResponse<string> >(
          `/product/${payload.id}`, payload);
        if (data.status) {
          return Promise.resolve('OK');
        } else {
          return Promise.resolve(data.message);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [DELETE_PRODUCT]({ commit }, payload: IProductDetailItem): Promise<string> {
      try {
        const { data } = await httpRequestSilence.delete<IResponse<string> >(
          `/product/${payload.id}`);
        if (data.status) {
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
    },
    [MODIFY_CUR_PRODUCT](state, payload: IProductDetailItem) {
      state.curProduct = payload;
    }
  },
  getters: {
    [GET_ALL_PRODUCTS](state): IProductDetailItem[] {
      return state.allProducts;
    },
    [GET_CUR_SHOP_PRODUCTS](state): IProductDetailItem[] {
      return state.curShopProducts;
    },
    [GET_CUR_PRODUCT](state): IProductDetailItem | null {
      return state.curProduct;
    }
  }
} as Module<State, any>;
