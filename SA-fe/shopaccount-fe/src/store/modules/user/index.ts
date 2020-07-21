import { Module } from 'vuex';
import { State } from './typings';
import {
  CURRENT_USER_INFO,
  LOAD_USER_PROFILE,
  MODIFY_USER_PROFILE,
  MODIFY_USER_IMG,
  MODIFY_USER_PHONE,
  UPADTE_USER_PASSWORD,
  UPADTE_USER_PHONE,
  CHECK_USERNAME_EXIST,
  CHECK_PHONE_EXIST,
  IS_LOGIN,
  LOGIN,
  LOGOUT,
  SIGNUP,
  UID,
  UIMG
} from './constants';
import { httpRequestSilence } from '@/utils/httpRequest';
import { IResponse } from '@/typing/vuex/typings';
import { SignUpForm, LoginForm } from '@/typing/login/typings';
import { ChangePdForm, UserInfo, ChangePhoneForm } from '@/typing/profile/typings';

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
        IResponse<UserInfo, {}>
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
    async [UPADTE_USER_PHONE]({ commit }, payload: ChangePhoneForm) {
      try {
        const { data } = await httpRequestSilence.put<
          IResponse<{}> >(`/userPhone`, payload);
        if (data.status) {
          commit(MODIFY_USER_PHONE, payload);
          return Promise.resolve('OK');
        } else {
          return Promise.resolve(data.message);
        }
      } catch (error) {
        return Promise.resolve(error);
      }
    },
    async [UPADTE_USER_PASSWORD]({ commit }, payload: ChangePdForm) {
      try {
        const { data } = await httpRequestSilence.put<
          IResponse<{}> >(`/userPassword`, payload);
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
    [MODIFY_USER_PHONE](state, payload: string) {
      if (state.user) {
        state.user.phone = payload;
      }
    },
    [MODIFY_USER_IMG](state, payload: string) {
      if (state.user) {
        state.user.img = payload;
      }
    },
    [MODIFY_USER_PROFILE](state, payload: UserInfo) {
      state.user = payload;
    }
  },
  getters: {
    [CURRENT_USER_INFO](state): UserInfo | null {
      return state.user;
    },
    [IS_LOGIN](state): boolean {
      return state.user !== null;
    },
    [UID](state): number | null {
      return state.user && state.user.id;
    },
    [UIMG](state): string {
      return (state.user && state.user.img) || 'default-user.jpg';
    }
  }
} as Module<State, any>;
