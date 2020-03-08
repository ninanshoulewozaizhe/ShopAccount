import { Module } from 'vuex';
import { State, IUserInfo } from './typings';
import {
  CURRENT_USER_INFO,
  LOAD_USER_PROFILE,
  MODIFY_USER_PROFILE,
  CHECK_USERNAME_EXIST,
  CHECK_PHONE_EXIST,
  IS_LOGIN,
  LOGIN,
  LOGOUT,
  SIGNUP,
  UID
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
    async [CHECK_USERNAME_EXIST]({ dispatch }, payload: string) {
      try {
        const { data } = await httpRequestSilence.get<
          IResponse<{}> >(`/register?username=${payload}`);
        if (data.status) {
          return Promise.resolve('exist');
        } else {
          return Promise.resolve('not exist');
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [CHECK_PHONE_EXIST]({ dispatch }, payload: string) {
      try {
        const { data } = await httpRequestSilence.get<
          IResponse<{}> >(`/checkPhone?phone=${payload}`);
        if (data.status) {
          return Promise.resolve('exist');
        } else {
          return Promise.resolve('not exist');
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
        >(`/login`);
        if (data.status) {
          commit(MODIFY_USER_PROFILE, data.data);
          return Promise.resolve('OK');
        } else {
          return Promise.resolve(data.message);
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
  mutations: {
    [MODIFY_USER_PROFILE](state, payload: IUserInfo) {
      state.user = payload;
    }
  },
  getters: {
    [CURRENT_USER_INFO](state): IUserInfo | null {
      return state.user;
    },
    [IS_LOGIN](state): boolean {
      return state.user !== null;
    },
    [UID](state): number | null {
      return state.user && state.user.id;
    }
  }
} as Module<State, any>;
