import { Module } from 'vuex';
import { State } from './typings';
import {
  GET_CUR_SHOP_TODAY_SALES,
  GET_CUR_SHOP_PERIOD_SALES,
  GET_CUR_PRODUCT_TODAY_SALES,
  GET_CUR_PRODUCT_YESTERDAY_SALES,
  GET_PRODUCT_ONE_DAY_SALES,
  GET_PRODUCT_PERIOD_SALES,
  GET_ALL_SHOPS_TODAY_SALES,
  GET_ALL_SHOPS_SALES_RANK,
  MODIFY_CUR_SHOP_PERIOD_SALES,
  MODIFY_CUR_SHOP_TODAY_SALES,
  MODIFY_CUR_PRODUCT_TODAY_SALES,
  MODIFY_CUR_PRODUCT_YESTERDAY_SALES,
  MODIFY_PRODUCT_ONE_DAY_SALES,
  MODIFY_PRODUCT_PERIOD_SALES,
  MODIFY_ALL_SHOPS_TODAY_SALES,
  MODIFY_ALL_SHOPS_SALES_RANK,
  LOAD_CUR_SHOP_PERIOD_SALES,
  LOAD_CUR_SHOP_TODAY_SALES,
  LOAD_CUR_PRODUCT_TODAY_SALES,
  LOAD_CUR_PRODUCT_YESTERDAY_SALES,
  LOAD_PRODUCT_ONE_DAY_SALES,
  LOAD_PRODUCT_PERIOD_SALES,
  LOAD_ALL_SHOPS_TODAY_SALES,
  LOAD_ALL_SHOPS_SALES_RANK,
  UPDATE_PRODUCT_ONE_DAY_SALES
} from './constants';
import { httpRequestSilence } from '@/utils/httpRequest';
import { IResponse } from '@/typing/vuex/typings';
import { SalesRecordItem, ShopsSalesItem } from '@/typing/salesStatus/typings';

export default {
  namespaced: true,
  state: () => ({
    curShopPeriodSales: [],
    curShopTodaySales: [],
    curProductTodaySales: null,
    curProductYesterdaySales: null,
    productOneDaySales: null,
    curProductPeriodSales: [],
    allShopsTodaySales: null,
    productsSalesRank: []
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
          commit(MODIFY_CUR_SHOP_TODAY_SALES, []);
          return Promise.resolve(data.message);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [LOAD_CUR_PRODUCT_TODAY_SALES]({ commit }, payload: any): Promise<string> {
      try {
        const { data } = await httpRequestSilence.get<IResponse<SalesRecordItem> >(
          `/salesRecord/${payload.pid}?date=${payload.date}`
        );
        if (data.status) {
          console.log(data);
          commit(MODIFY_CUR_PRODUCT_TODAY_SALES, data.data);
          return Promise.resolve('OK');
        } else {
          commit(MODIFY_CUR_PRODUCT_TODAY_SALES, null);
          return Promise.resolve(data.message);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [LOAD_CUR_PRODUCT_YESTERDAY_SALES]({ commit }, payload: any): Promise<string> {
      try {
        const { data } = await httpRequestSilence.get<IResponse<SalesRecordItem> >(
          `/salesRecord/${payload.pid}?date=${payload.date}`
        );
        if (data.status) {
          console.log(data);
          commit(MODIFY_CUR_PRODUCT_YESTERDAY_SALES, data.data);
          return Promise.resolve('OK');
        } else {
          commit(MODIFY_CUR_PRODUCT_YESTERDAY_SALES, null);
          return Promise.resolve(data.message);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [LOAD_PRODUCT_ONE_DAY_SALES]({ commit }, payload: any): Promise<string> {
      try {
        const { data } = await httpRequestSilence.get<IResponse<SalesRecordItem> >(
          `/salesRecord/${payload.pid}?date=${payload.date}`
        );
        if (data.status) {
          console.log(data);
          commit(MODIFY_PRODUCT_ONE_DAY_SALES, data.data);
          return Promise.resolve('OK');
        } else {
          commit(MODIFY_PRODUCT_ONE_DAY_SALES, null);
          return Promise.resolve(data.message);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [UPDATE_PRODUCT_ONE_DAY_SALES]({ commit }, payload: any): Promise<string> {
      try {
        const { data } = await httpRequestSilence.put<IResponse<string> >(
          `/salesRecord/${payload.pid}`, payload
        );
        if (data.status) {
          return Promise.resolve('OK');
        } else {
          return Promise.resolve(data.message);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [LOAD_CUR_SHOP_PERIOD_SALES]({ commit }, payload: any): Promise<string> {
      try {
        const { data } = await httpRequestSilence.get<IResponse<SalesRecordItem[]> >(
          `/shopSalesPeriod/${payload.sid}?from=${payload.from}&to=${payload.to}`
        );
        if (data.status) {
          commit(MODIFY_CUR_SHOP_PERIOD_SALES, data.data);
          return Promise.resolve('OK');
        } else {
          commit(MODIFY_CUR_SHOP_PERIOD_SALES, []);
          return Promise.resolve(data.message);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [LOAD_PRODUCT_PERIOD_SALES]({ commit }, payload: any): Promise<string> {
      try {
        const { data } = await httpRequestSilence.get<IResponse<SalesRecordItem[]> >(
          `/salesRecordsPeriod/${payload.pid}?from=${payload.from}&to=${payload.to}`
        );
        if (data.status) {
          commit(MODIFY_PRODUCT_PERIOD_SALES, data.data);
          return Promise.resolve('OK');
        } else {
          commit(MODIFY_PRODUCT_PERIOD_SALES, []);
          return Promise.resolve(data.message);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [LOAD_ALL_SHOPS_TODAY_SALES]({ commit }, payload: any): Promise<string> {
      try {
        const { data } = await httpRequestSilence.get<IResponse<ShopsSalesItem> >(
          `/salesRecordsPeriod/${payload.pid}?from=${payload.from}&to=${payload.to}`
        );
        if (data.status) {
          commit(MODIFY_ALL_SHOPS_TODAY_SALES, data.data);
          return Promise.resolve('OK');
        } else {
          commit(MODIFY_ALL_SHOPS_TODAY_SALES, null);
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
    [MODIFY_CUR_SHOP_PERIOD_SALES](state, payload: SalesRecordItem[]) {
      state.curShopPeriodSales = payload;
    },
    [MODIFY_CUR_PRODUCT_TODAY_SALES](state, payload: SalesRecordItem | null) {
      state.curProductTodaySales = payload;
    },
    [MODIFY_CUR_PRODUCT_YESTERDAY_SALES](state, payload: SalesRecordItem | null) {
      state.curProductYesterdaySales = payload;
    },
    [MODIFY_PRODUCT_ONE_DAY_SALES](state, payload: SalesRecordItem | null) {
      state.productOneDaySales = payload;
    }
  },
  getters: {
    [GET_CUR_SHOP_TODAY_SALES](state): SalesRecordItem[] {
      return state.curShopTodaySales;
    },
    [GET_CUR_SHOP_PERIOD_SALES](state): SalesRecordItem[] {
      return state.curShopPeriodSales;
    },
    [GET_CUR_PRODUCT_TODAY_SALES](state): SalesRecordItem | null {
      return state.curProductTodaySales;
    },
    [GET_CUR_PRODUCT_YESTERDAY_SALES](state): SalesRecordItem | null {
      return state.curProductYesterdaySales;
    },
    [GET_PRODUCT_ONE_DAY_SALES](state): SalesRecordItem | null {
      return state.productOneDaySales;
    }
  }
} as Module<State, any>;
