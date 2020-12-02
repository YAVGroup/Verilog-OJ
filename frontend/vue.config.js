// vue.config.js
module.exports = {
    publicPath: process.env.NODE_ENV === 'production'
        ? '/oj/'
        : '/',

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