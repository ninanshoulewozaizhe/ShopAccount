import { Module } from 'vuex';
import { State } from './typings';
import {
  GET_ALL_SHOPS,
  GET_CUR_SHOP,
  MODIFY_ALL_SHOPS,
  MODIFY_CUR_SHOP,
  LOAD_ALL_SHOPS,
  LOAD_CUR_SHOP,
  ADD_NEW_SHOP,
  DELETE_SHOP,
  UPDATE_SHOP
} from './constants';
import { httpRequestSilence } from '@/utils/httpRequest';
import { IResponse } from '@/typing/vuex/typings';
import { IShopItem, IShopPreItem } from '@/typing/shops/typings';


export default {
  namespaced: true,
  state: () => ({
    allShops: [],
    curShop: null
  }),
  actions: {
    async [LOAD_ALL_SHOPS]({ commit }): Promise<string> {
      try {
        const { data } = await httpRequestSilence.get<IResponse<IShopPreItem[]> >(
          `/shops`
        );
        if (data.status) {
          commit(MODIFY_ALL_SHOPS, data.data);
          return Promise.resolve('OK');
        } else {
          return Promise.resolve(data.message);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [LOAD_CUR_SHOP]({ commit }, payload: number): Promise<string> {
      try {
        const { data } = await httpRequestSilence.get<IResponse<IShopItem> >(
          `/shop/${payload}`);
        if (data.status) {
          commit(MODIFY_CUR_SHOP, data.data);
          return Promise.resolve('OK');
        } else {
          return Promise.resolve(data.message);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [ADD_NEW_SHOP]({ commit }, payload: IShopItem): Promise<any> {
      try {
        const { data } = await httpRequestSilence.post<IResponse<any> >(
          `/createShop`, payload);
        if (data.status) {
          return Promise.resolve({status: true, sid: data.data.sid});
        } else {
          return Promise.resolve(data.message);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [UPDATE_SHOP]({ commit }, payload: IShopItem): Promise<string> {
      try {
        const { data } = await httpRequestSilence.put<IResponse<string> >(
          `/shop/${payload.id}`, payload);
        if (data.status) {
          return Promise.resolve('OK');
        } else {
          return Promise.resolve(data.message);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [DELETE_SHOP]({ commit }, payload: IShopItem): Promise<string> {
      try {
        const { data } = await httpRequestSilence.delete<IResponse<string> >(
          `/shops/${payload.id}`);
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
    [MODIFY_ALL_SHOPS](state, payload: IShopPreItem[]) {
      state.allShops = payload;
    },
    [MODIFY_CUR_SHOP](state, payload: IShopPreItem) {
      state.curShop = payload;
    },
    [ADD_NEW_SHOP](state, payload: IShopPreItem) {
      state.allShops.push(payload);
    }
  },
  getters: {
    [GET_ALL_SHOPS](state): IShopPreItem[] {
      return state.allShops;
    },
    [GET_CUR_SHOP](state): IShopItem | null {
      return state.curShop;
    }
  }
} as Module<State, any>;
