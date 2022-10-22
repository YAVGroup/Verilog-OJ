import Vue from "vue";
import Router from "vue-router";

const originalPush = Router.prototype.push;
Router.prototype.push = function push(location, onResolve, onReject) {
  if (onResolve || onReject)
    return originalPush.call(this, location, onResolve, onReject);
  return originalPush.call(this, location).catch((err) => err);
};

// Regarding "() => import(...)" stuff, check out this:
// https://router.vuejs.org/guide/advanced/lazy-loading.html#grouping-components-in-the-same-chunk

Vue.use(Router);

export default new Router({
  mode: "history",

  // Ref: https://cli.vuejs.org/guide/mode-and-env.html#using-env-variables-in-client-side-code
  // This resolves to /oj/ in production while resolves to / in development,
  // as is set in vue.config.js

  base: process.env.BASE_URL,
  routes: [
    // 主界面
    {
      path: "/",
      name: "homepage",
      component: () =>
        import( /* webpackChunkName: "main" */ "@/components/main"),
    },

    // Learn
    {
      path: "/learn/",
      name: "learn",
      component: () =>
        import(
          /* webpackChunkName: "learn" */
          "@/components/mainpage/learn"
        ),
    },

    {
      path: "/learn/:bookid",
      name: "learndetail",
      component: () =>
        import(
          /* webpackChunkName: "learn" */
          "@/components/mainpage/learndetail"
        ),
    },

    // News
    {
      path: "/newsdetail/:newsid",
      name: "newsdetail",
      component: () =>
        import(
          /* webpackChunkName: "main" */
          "@/components/mainpage/newsdetail"
        ),
    },

    // 用户信息及修改
    {
      path: "/user/:userid",
      name: "user",
      component: () =>
        import( /* webpackChunkName: "user" */ "@/components/mainpage/user"),
    },
    {
      path: "/setting",
      name: "setting",
      component: () =>
        import( /* webpackChunkName: "user" */ "@/components/mainpage/setting"),
    },

    // 题目列表和题目细节
    {
      path: "/problempage/:pageid",
      name: "problem",
      component: () =>
        import(
          /* webpackChunkName: "problem" */
          "@/components/mainpage/problem"
        ),
    },

    //题目添加
    {
      path: "/problem/:problemid/edit",
      name: "problemedit",
      component: () =>
        import(
          /* webpackChunkName: "problem" */
          "@/components/problem/problemedit"
        ),
    },

    {
      path: "/problem/add",
      name: "addproblem",
      component: () =>
        import(
          /* webpackChunkName: "problem" */
          "@/components/problem/problemedit"
        ),
    },

    {
      path: "/problem/:problemid",
      name: "problemdetail",
      component: () =>
        import(
          /* webpackChunkName: "problem" */
          "@/components/problem/problemdetail"
        ),
    },

    // 讨论区
    {
      path: "/discussion/:problemid",
      name: "discussion",
      component: () =>
        import(
          /* webpackChunkName: "problem" */
          "@/components/mainpage/discussion"
        ),
    },
    {
      path: "/topic/:topicid",
      name: "topic",
      component: () =>
        import(
          /* webpackChunkName: "problem" */
          "@/components/mainpage/topic"
        ),
    },

    // 提交列表和提交细节
    {
      path: "/statue",
      name: "statue",
      component: () =>
        import(
          /* webpackChunkName: "problem" */
          "@/components/mainpage/statue"
        ),
    },
    {
      path: "/submission/:submissionid",
      name: "submission",
      component: () =>
        import(
          /* webpackChunkName: "problem" */
          "@/components/mainpage/submission"
        ),
    },

    // 组合逻辑向导
    {
      path: "/guide/combinational",
      name: "combGuide",
      component: () => import("@/components/guide/combinational")
    },

    // 管理员界面
    {
      path: "/admin",
      name: "admin",
      component: () =>
        import( /* webpackChunkName: "admin" */ "@/components/mainpage/admin"),
    },

    // 404 Page
    {
      path: "*",
      component: () =>
        import( /* webpackChunkName: "err" */ "@/components/error/notfound"),
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
  ],
});
