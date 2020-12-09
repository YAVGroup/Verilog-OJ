import Vue from 'vue'
import Router from 'vue-router'

// Regarding "() => import(...)" stuff, check out this:
// https://router.vuejs.org/guide/advanced/lazy-loading.html#grouping-components-in-the-same-chunk

Vue.use(Router)

export default new Router({
  mode: 'history',

  // Ref: https://cli.vuejs.org/guide/mode-and-env.html#using-env-variables-in-client-side-code
  // This resolves to /oj/ in production while resolves to / in development,
  // as is set in vue.config.js

  base: process.env.BASE_URL,
  routes: [
    // 主界面
    {
      path: '/',
      name: 'homepage',
      component: () => import(/* webpackChunkName: "main" */ "@/components/main")
    },

    // News
    {
      path: '/newsdetail/:newsid',
      name: 'newsdetail',
      component: () => import(/* webpackChunkName: "main" */ "@/components/mainpage/newsdetail")
    },

    // 用户信息及修改
    {
      path: '/user/:userid',
      name: 'user',
      component: () => import(/* webpackChunkName: "user" */ "@/components/mainpage/user")
    },
    {
      path: '/setting',
      name: 'setting',
      component: () => import(/* webpackChunkName: "user" */ "@/components/mainpage/setting")
    },

    // 题目列表和题目细节
    {
      path: '/problem',
      name: 'problem',
      component: () => import(/* webpackChunkName: "problem" */ "@/components/mainpage/problem")
    },
    {
      path: '/problemdetail/:problemid',
      name: 'problemdetail',
      component: () => import(/* webpackChunkName: "problem" */ "@/components/problem/problemdetail")
    },

    // 提交列表和提交细节
    {
      path: '/statue',
      name: 'statue',
      component: () => import(/* webpackChunkName: "problem" */ "@/components/mainpage/statue")
    },
    {
      path: '/submission/:submissionid',
      name: 'submission',
      component: () => import(/* webpackChunkName: "problem" */ "@/components/mainpage/submission")
    },

    // 管理员界面
    {
      path: '/admin',
      name: 'admin',
      component: () => import(/* webpackChunkName: "admin" */ "@/components/mainpage/admin")
    },

    // 404 Page
    {
      path: '*',
      component: () => import(/* webpackChunkName: "err" */ "@/components/error/notfound")
    }
  //   {
  //     path: '/contest',
  //     name: 'contest',
  //     component: contest
  //   },
  //   {
  //     path: '/contest/:contestID',
  //     name: 'contestdetail',
  //     component: contestdetail,
  //   },
  //   {
  //     path: '/rank',
  //     name: 'rank',
  //     component: rank,
  //   },
  //   {
  //     path: '/classdetail',
  //     name: 'classdetail',
  //     component: classdetail,
  //   },
  //   {
  //     path: '/classes',
  //     name: 'classes',
  //     component: classes,
  //   },
  //   {
  //     path: '/homework',
  //     name: 'homework',
  //     component: homework,
  //   }
  ]
})
