// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Vuex from 'vuex'
import md5 from 'js-md5';
import axios from 'axios';
import VueClipboard from 'vue-clipboard2'
import 'babel-polyfill' //兼容IE6
import Cookies from 'js-cookie'

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(ElementUI);


import { ExpansionPanel } from 'muse-ui';
Vue.use(ExpansionPanel);


Vue.use(VueClipboard)
Vue.use(Vuex)

Vue.config.productionTip = false
Vue.prototype.$md5 = md5;

//开启debug模式
Vue.config.debug = true;
axios.defaults.withCredentials = true;
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.baseURL = process.env.API_ROOT
Vue.prototype.$axios = axios;

const store = new Vuex.Store({
  state: {
    loginip:"后台获取",
    logininfo:"后台获取"
  },
})

// 根据cookie里设置的userid，获取用户信息；但这个是异步的，可能需要刷新一下页面
const userid = Cookies.get('userid');
if (userid == undefined) {
  sessionStorage.setItem("userid", "");
  sessionStorage.setItem("username", "");
  sessionStorage.setItem("name", "");
  sessionStorage.setItem("is_admin", false);
} else {
  if(sessionStorage.getItem("userid") == undefined || sessionStorage.getItem("userid") == ""){
    sessionStorage.setItem("userid", userid);
    axios.get("/users/" + userid + "/").then(response => {
      sessionStorage.setItem("username", response.data.username);
      var name = response.data.last_name+response.data.first_name;
      if(name == "")
        name = response.data.username;
      sessionStorage.setItem("name", name);
      sessionStorage.setItem("isadmin", response.data.is_superuser);
    })
  }
}

new Vue({
  el: '#app',
  router,
  components: { App },
  store,
  template: '<App/>',
  render: h => h(App),
  created() {

  }
})

