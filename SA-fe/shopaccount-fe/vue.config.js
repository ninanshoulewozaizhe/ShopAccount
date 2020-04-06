module.exports = {
    devServer: {
      proxy: {
        '/api': {
          target: 'http://129.204.148.253:5000',
          ws: true,
          changeOrigin: true
        }
      }
      // proxy: 'http://127.0.0.1:5000'
    }
}
