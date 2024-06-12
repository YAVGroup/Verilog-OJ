// vue.config.js
module.exports = {
  // In VLab environment, we use vlab.ustc.edu.cn/oj/... to access
  publicPath: process.env.NODE_ENV === "production" ? "/oj/" : "/",

  assetsDir: "",

  // Used to forward API requests to Django
  devServer: {
    proxy: {
      "/oj/api": {
        target: process.env.VERILOG_OJ_DEV_CONTAINER_USED == "yes" ? 
                "http://backend:8000/oj/api" : "http://localhost:8000/oj/api",
        changeOrigin: true,
        pathRewrite: {
          "^/oj/api": "/",
        },
      },
    },
  },
};
