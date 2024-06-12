// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import App from "./App";
import router from "./router";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";
import axios from "axios";
import VueClipboard from "vue-clipboard2";
//import 'babel-polyfill' //兼容IE6
import Cookies from "js-cookie";

import "./assets/site.css";

import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
Vue.use(ElementUI);

Vue.use(VueClipboard);
Vue.use(Vuex);

Vue.config.productionTip = false;

//开启debug模式
Vue.config.debug = true;
axios.defaults.withCredentials = true;
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";
// This will be bundled by Vue CLI
axios.defaults.baseURL = process.env.VUE_APP_API_ROOT;
Vue.prototype.$axios = axios;

const store = new Vuex.Store({
  plugins: [
    createPersistedState({
      storage: sessionStorage,
    }),
  ],
  state: {
    // -- account related --
    loggedIn: false,
    userID: 0,
    username: "",
    isSuperUser: false,
    isPasswordStrong: false
  },
  mutations: {
    logIn(state, payload) {
      state.loggedIn = true;
      state.userID = payload.userID;
      state.username = payload.username;
      state.isSuperUser = payload.isSuperUser;
      state.isPasswordStrong = payload.isPasswordStrong;
    },
    logOut(state) {
      state.loggedIn = false;
      state.userID = 0;
      state.username = "";
      state.isSuperUser = false;
      state.isPasswordStrong = false;
    },
    // Will be called when password vulnerability have fixed
    markPasswordStrong(state) {
      state.isPasswordStrong = true;
    }
  },
  actions: {
    /**
     * Log into the system.
     * @param {*} context
     * @param {*} payload - contains { username, password, success_cb, fail_cb }
     */
    logIn(context, payload) {
      axios
        .post("/user/login/", {
          username: payload.username,
          password: payload.password,
        })
        .then((response) => {
          payload.success_cb(response);
          context.commit({
            type: "logIn",
            userID: response.data.id,
            username: response.data.username,
            isSuperUser: response.data.is_superuser,
            isPasswordStrong: response.data.is_password_strong
          });
        })
        .catch((error) => {
          payload.fail_cb(error);
        });
    },
    /**
     * Log out the system.
     * @param {*} context
     * @param {*} payload - contains { username, password, success_cb, fail_cb }
     */
    logOut(context, payload) {
      axios
        .get("/user/logout/")
        .then((response) => {
          payload.success_cb(response);
          context.commit({
            type: "logOut",
          });
        })
        .catch((error) => {
          payload.fail_cb(error);
        });
    },
    /**
     * This is used when page refresh happens, mostly happening during CAS login
     * @param {*} context
     * @param {*} payload
     */
    refreshLogInStatus(context, payload) {
      axios.get("/user/status-login").then((response) => {
        if (
          response.data.isLoggedIn &&
          response.data.userID != this.state.userID
        ) {
          console.log("[ INFO ] Login state invalidated, do logIn");
          context.commit({
            type: "logIn",
            userID: response.data.userID,
            username: response.data.username,
            isSuperUser: response.data.isSuperUser,
            isisPasswordStrong: response.data.isPasswordStrong
          });
        } else if (!response.data.isLoggedIn && this.state.loggedIn) {
          console.log("[ INFO ] Login state invalidated, do logOut");
          context.commit({
            type: "logOut",
          });
        }
      });
    },
  },
});

new Vue({
  el: "#app",
  router,
  components: { App },
  store: store,
  template: "<App/>",
  render: (h) => h(App),
  created() {
    // check if we've been logged in (e.g. cas)
    this.$store.dispatch("refreshLogInStatus");
  },
});
