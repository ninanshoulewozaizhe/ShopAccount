import { Module } from 'vuex';

export type ModuleState<M> = M extends Module<infer S, any> ? S : {};

export type ActionObject<P = object> = { type: string } & {
  [Key in keyof P]: P[Key];
};

export interface IResponse<D, P = {}> {
  data?: D;
  message: string;
  paramData: P;
  status: boolean;
  time: string;
}

