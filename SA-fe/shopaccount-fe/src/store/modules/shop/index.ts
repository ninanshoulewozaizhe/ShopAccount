import { Module } from 'vuex';
import { State } from './typings';
import {
  GET_ALL_SHOPS,
  MODIFY_ALL_SHOPS,
  LOAD_ALL_SHOPS,
  ADD_NEW_SHOP
} from './constants';
import { httpRequestSilence } from '@/utils/httpRequest';
import { IResponse } from '@/typing/vuex/typings';
import { IShopItem } from '@/typing/shops/typings';
import { IProductItem } from '@/typing/home/typings';


export default {
  namespaced: true,
  state: () => ({
    allShops: []
  }),
  actions: {
    async [LOAD_ALL_SHOPS]({ commit }): Promise<string> {
      try {
        const { data } = await httpRequestSilence.get<IResponse<IShopItem[]> >(
          `/shops`
        );
        if (data.status || data.msg === 'OK') {
          commit(MODIFY_ALL_SHOPS, data.data);
          return Promise.resolve('OK');
        } else {
          return Promise.resolve(data.msg);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [ADD_NEW_SHOP]({ commit }, payload: IShopItem): Promise<string> {
      try {
        const { data } = await httpRequestSilence.post<IResponse<IShopItem[]> >(
          `/shops`, payload);
        if (data.status || data.msg === 'OK') {
          commit(MODIFY_ALL_SHOPS, data.data);
          return Promise.resolve('OK');
        } else {
          return Promise.resolve(data.msg);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    }

  },
  mutations: {
    [MODIFY_ALL_SHOPS](state, payload: IShopItem[]) {
      state.allShops = payload;
    },
    [ADD_NEW_SHOP](state, payload: IShopItem) {
      state.allShops.push(payload);
    }
  },
  getters: {
    [GET_ALL_SHOPS](state): IShopItem[] {
      return state.allShops;
    }
  }
} as Module<State, any>;
