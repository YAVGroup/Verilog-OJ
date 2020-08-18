import Vue from 'vue'
import Router from 'vue-router'

const homepage = r => require.ensure([], () => r(require("@/components/main")), 'main"');
const problem = r => require.ensure([], () => r(require("@/components/mainpage/problem")), 'mainpage');
const statue = r => require.ensure([], () => r(require("@/components/mainpage/statue")), 'mainpage');
const user = r => require.ensure([], () => r(require("@/components/mainpage/user")), 'mainpage');
const setting = r => require.ensure([], () => r(require("@/components/mainpage/setting")), 'mainpage');
const contest = r => require.ensure([], () => r(require("@/components/mainpage/contest")), 'mainpage');
const contestdetail = r => require.ensure([], () => r(require("@/components/contest/contestdetail")), 'contest');
const problemdetail = r => require.ensure([], () => r(require("@/components/problem/problemdetail")), 'problem');
const rank = r => require.ensure([], () => r(require("@/components/mainpage/rank")), 'mainpage');
const admin = r => require.ensure([], () => r(require("@/components/mainpage/admin")), 'mainpage');
const homework = r => require.ensure([], () => r(require("@/components/mainpage/homework")), 'mainpage');
const classes = r => require.ensure([], () => r(require("@/components/mainpage/classes")), 'mainpage');
const classdetail = r => require.ensure([], () => r(require("@/components/mainpage/classdetail")), 'mainpage');
const submission = r => require.ensure([], () => r(require("@/components/mainpage/submission")), 'mainpage');


Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    // 主界面
    {
      path: '/',
      name: 'homepage',
      component: homepage
    },

    // 用户信息及修改
    {
      path: '/user/:userid',
      name: 'user',
      component: user
    },
    {
      path: '/setting',
      name: 'setting',
      component: setting
    },

    // 题目列表和题目细节
    {
      path: '/problem',
      name: 'problem',
      component: problem,
    },
    {
      path: '/problemdetail/:problemid',
      name: 'problemdetail',
      component: problemdetail,
    },

    // 提交列表和提交细节
    {
      path: '/statue',
      name: 'statue',
      component: statue
    },
    {
      path: '/submission/:submissionid',
      name: 'submission',
      component: submission
    },

    // 管理员界面
    {
      path: '/admin',
      name: 'admin',
      component: admin
    },

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
