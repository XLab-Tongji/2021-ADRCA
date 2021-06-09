
module.exports = {
    publicPath: './',
    //配置跨域请求
    devServer: {
        host: 'localhost',
        port: 8082,    //启动端口号
        https: false,    //是否开启https
        hotOnly: false,
        proxy: { // 配置跨域
            '/api': {
                target: 'http://10.60.38.173:5002',
                changOrigin: true,
                pathRewrite: {
                    '^/api': ''
                }
            }
            
            
        }
    }
};
