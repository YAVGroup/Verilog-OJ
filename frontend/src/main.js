// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import App from './App';
import router from './router';
import Vuex from 'vuex';
import createPersistedState from "vuex-persistedstate";
import axios from 'axios';
import VueClipboard from 'vue-clipboard2'
//import 'babel-polyfill' //兼容IE6
import Cookies from 'js-cookie'

import './assets/site.css';

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(ElementUI);

Vue.use(VueClipboard)
Vue.use(Vuex)

Vue.config.productionTip = false

//开启debug模式
Vue.config.debug = true;
axios.defaults.withCredentials = true;
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";
// This will be bundled by Vue CLI
axios.defaults.baseURL = process.env.VUE_APP_API_ROOT
Vue.prototype.$axios = axios;

const store = new Vuex.Store({
  plugins: [createPersistedState({
    storage: sessionStorage
  })],
  state: {
    // -- account related --
    loggedIn: false,
    userID: 0,
    username: "",
    isSuperUser: false
  },
  mutations: {
    logIn (state, payload) {
      state.loggedIn = true;
      state.userID = payload.userID;
      state.username = payload.username;
      state.isSuperUser = payload.isSuperUser;
    },
    logOut (state) {
      state.loggedIn = false;
      state.userID = 0;
      state.username = "";
      state.isSuperUser = false;
    }
  },
  actions: {
    /**
     * Log into the system.
     * @param {*} context 
     * @param {*} payload - contains { username, password, success_cb, fail_cb }
     */
    logIn (context, payload) {
      axios.post("/user/login/", {
          username: payload.username,
          password: payload.password
      })
      .then(response => {
        payload.success_cb(response);
        context.commit({
          type: 'logIn',
          userID: response.data.id,
          username: response.data.username,
          isSuperUser: response.data.is_superuser
        })
        this.dialogLoginVisible = false;
      })
      .catch(error => {
        payload.fail_cb(error);
      });
    }
  }
})

new Vue({
  el: '#app',
  router,
  components: { App },
  store: store,
  template: '<App/>',
  render: h => h(App),
  created() {

  }
})

