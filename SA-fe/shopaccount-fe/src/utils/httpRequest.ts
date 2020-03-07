import axios, { AxiosResponse } from 'axios';

const instanceConfig = {
  timeout: 5000
};

export const httpRequest = axios.create(instanceConfig); // 请求对象，通常情况下使用此请求器
export const httpRequestSilence = axios.create(instanceConfig); // 请求对象，但不会在错误的时候调用 Notification

httpRequest.interceptors.response.use(
  (response) => response,
  (error): Promise<AxiosResponse<any>> => {
    const { response, config, code } = error;
    const message = `${config.method.toUpperCase()} ${config.url}`;
    if (response && response.status === 401) {
      // Notification.error({
      //   title: '尚未登录',
      //   message: '请登录后再尝试',
      //   offset: 60
      // });
      // router.push({ name: 'home' });
    } else if (code && code === 'ECONNABORTED') {
      // Notification.error({
      //   title: '请求超时',
      //   message,
      //   offset: 60
      // });
    } else {
      // Notification.error({
      //   title: (response && response.data && response.data.msg) || `请求错误`,
      //   message,
      //   offset: 60
      // });
    }
    return Promise.reject<AxiosResponse<any>>(response);
  }
);

httpRequestSilence.interceptors.response.use(
  (response) => response,
  (error): Promise<AxiosResponse<any>> => {
    const { response } = error;
    return Promise.reject<AxiosResponse<any>>(response);
  }
);
