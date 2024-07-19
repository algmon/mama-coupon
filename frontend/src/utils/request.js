import axios from "axios";
import { MessageBox, Message } from "element-ui";
import store from "@/store";
import { getToken } from "@/utils/auth";


function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 300000, // request timeout
  headers: {
    "token": getCookie('token'),
  }
});

// request interceptor
// service.interceptors.request.use(
//   (config) => {
//     // do something before request is sent
//     // // 获取所有的cookie
//     const cookies = document.cookie.split(";");

//     // console.log("cookies:>>>>>>>>>>>>>>>>>", cookies);
//     // console.log("cookies.length:================", cookies.length);

//     for (let i = 0; i < cookies.length; i++) {
//       // 去除每个cookie字符串的首尾空白字符
//       const cookie = cookies[i].trim();
//       // console.log("cookies:", cookie);
//       // 检查当前cookie是否包含我们需要的键名
//       if (cookie.startsWith("token")) {
//         // 如果找到了，解码并返回该cookie的值
//         const token = cookie.substring("token".length + 1);
//         // console.log("tokenVaule:=====>>>>", token);
//         config.headers['token'] = token;
//         config.headers["Access-Control-Allow-Origin", "*"];
//       }
//       // if (store.getters.token) {
//       //   // let each request carry token
//       //   // ['X-Token'] is a custom headers key
//       //   // please modify it according to the actual situation
//       //   config.headers["X-Token"] = Cookies.get("token");
//       //   console.log("token:", Cookies.get("token"));
//       // }
//     }
//     return config;
//   },
//   (error) => {
//     // do something with request error
//     console.log(error); // for debug
//     return Promise.reject(error);
//   }
// );

// response interceptor
service.interceptors.response.use();

export default service;
