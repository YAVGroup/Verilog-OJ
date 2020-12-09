// vue.config.js
module.exports = {
    // In VLab environment, we use vlab.ustc.edu.cn/oj/... to access
    publicPath: process.env.NODE_ENV === 'production'
        ? '/oj/'
        : '/',

    assetsDir: '',

    // Used to forward API requests to Django
    devServer: {
        proxy: {
            '/api': {
                target: 'http://localhost:8000/api',
                changeOrigin: true,
                pathRewrite: {
                    '^/api': '/'
                }
            }
        }
    }
}