import { Module } from 'vuex';
import { State } from './typings';
import {
  GET_CUR_SHOP_TODAY_SALES,
  GET_CUR_SHOP_PEROID_SALES,
  MODIFY_CUR_SHOP_PEROID_SALES,
  MODIFY_CUR_SHOP_TODAY_SALES,
  LOAD_CUR_SHOP_PEROID_SALES,
  LOAD_CUR_SHOP_TODAY_SALES
} from './constants';
import { httpRequestSilence } from '@/utils/httpRequest';
import { IResponse } from '@/typing/vuex/typings';
import { SalesRecordItem, OneDaySalesItem } from '@/typing/salesStatus/typings';

export default {
  namespaced: true,
  state: () => ({
    curShopPeriodSales: [],
    curShopTodaySales: []
  }),
  actions: {
    async [LOAD_CUR_SHOP_TODAY_SALES]({ commit }, payload: any): Promise<string> {
      try {
        const { data } = await httpRequestSilence.get<IResponse<SalesRecordItem[]> >(
          `/shopSalesRecords/${payload.sid}?date=${payload.date}`
        );
        if (data.status) {
          commit(MODIFY_CUR_SHOP_TODAY_SALES, data.data);
          return Promise.resolve('OK');
        } else {
          return Promise.resolve(data.message);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [LOAD_CUR_SHOP_PEROID_SALES]({ commit }, payload: number): Promise<string> {
      try {
        const { data } = await httpRequestSilence.get<IResponse<OneDaySalesItem[]> >(
          `/products/${payload}`
        );
        if (data.status) {
          commit(MODIFY_CUR_SHOP_PEROID_SALES, data.data);
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
    [MODIFY_CUR_SHOP_TODAY_SALES](state, payload: SalesRecordItem[]) {
      state.curShopTodaySales = payload;
    },
    [MODIFY_CUR_SHOP_PEROID_SALES](state, payload: OneDaySalesItem[]) {
      state.curShopPeriodSales = payload;
    }
  },
  getters: {
    [GET_CUR_SHOP_TODAY_SALES](state): SalesRecordItem[] {
      return state.curShopTodaySales;
    },
    [GET_CUR_SHOP_PEROID_SALES](state): OneDaySalesItem[] {
      return state.curShopPeriodSales;
    }
  }
} as Module<State, any>;
