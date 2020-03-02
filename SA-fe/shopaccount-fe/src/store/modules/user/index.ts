import { Module } from 'vuex';
import { State, IUserInfo } from './typings';
import {
  CURRENT_USER_INFO,
  LOAD_USER_PROFILE,
  MODIFY_USER_PROFILE,
  IS_LOGIN,
  UID,
  LOGIN,
  LOGOUT,
  SIGNUP
} from './constants';
import { httpRequestSilence } from '@/utils/httpRequest';
import { IResponse } from '@/typing/vuex/typings';
import { SignUpForm, LoginForm } from '@/typing/login/typings';

export default {
  namespaced: true,
  state: () => ({
      user: null
  }),
  actions: {
    async [LOGIN]({ commit }, payload: LoginForm) {
      try {
        const { data } = await httpRequestSilence.post<
          IResponse<{}> >(`/login`, payload);
        if (data.status) {
          commit(MODIFY_USER_PROFILE, data.data);
          return Promise.resolve('OK');
        } else {
          return Promise.resolve('fail');
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [LOGOUT]({ commit }, payload) {
      try {
        const { data } = await httpRequestSilence.put<
          IResponse<{}> >(`/logout`);
        if (data.status) {
          commit(MODIFY_USER_PROFILE, null);
          return Promise.resolve('OK');
        } else {
          return Promise.resolve('fail');
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [SIGNUP]({ dispatch }, payload: SignUpForm) {
      try {
        const { data } = await httpRequestSilence.post<
          IResponse<{}> >(`/register`, payload);
        if (data.status) {
          return Promise.resolve('OK');
        } else {
          return Promise.resolve('fail');
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [LOAD_USER_PROFILE]({ commit }): Promise<string> {
      // noop
      try {
        const { data } = await httpRequestSilence.get<
        IResponse<IUserInfo, {}>
        >(`/user`);
        if (data.status) {
          commit(MODIFY_USER_PROFILE, data.data);
          return Promise.resolve('OK');
        } else {
          return Promise.resolve(data.msg);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [MODIFY_USER_PROFILE]({commit}, payload) {
      try {
        const { data } = await httpRequestSilence.put<
        IResponse<{}, {}>
        >(`/user`, payload);
        if (data.status) {
          commit(MODIFY_USER_PROFILE, payload);
          return data;
        }
      } catch (error) {
        return error.data;
      }
    }
  },
  getters: {
    [CURRENT_USER_INFO](state): IUserInfo | null {
      return state.user;
    },
    [IS_LOGIN](state): boolean {
      return state.user !== null;
    }
  }
} as Module<State, any>;
