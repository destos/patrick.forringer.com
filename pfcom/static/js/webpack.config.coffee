nib = require 'nib'
path = require 'path'
webpack = require 'webpack'
ExtractTextPlugin = require 'extract-text-webpack-plugin'

root = path.resolve(__dirname, '../../')

module.exports =
    context: __dirname
    entry: './main.coffee'
    output:
        path: '[bundle_dir]'
        filename: 'bundle-[hash].js'
        chunkFilename: '[id].js'
    module:
        loaders: [
            {test: /\.coffee$/, loader: 'coffee-loader'}
            {test: /\.(coffee\.md|litcoffee)$/, loader: "coffee-loader?literate"}
            {test: /\.styl$/, loader: ExtractTextPlugin.extract('style-loader', 'css-loader!stylus-loader')}
            {test: /\.less$/, loader: ExtractTextPlugin.extract('style-loader', 'css-loader!less-loader')}
            {test: /\.css$/, loader: ExtractTextPlugin.extract('style-loader', 'css-loader')}
        ]
    resolve:
        root: root
        # root: [ path.join(root, 'node_modules') ]
        modulesDirectories: ['node_modules', 'pfcom/static']
        # hangs when uncommented
        # extensions: ['', '.js', '.styl', '.coffee', '.coffee.md', '.litcoffee', '.css']
    # Stylus loader options
    stylus:
        use: [nib()]
        # import: ['variables', 'mixins']
    devtool: 'eval'

    plugins: [
        new webpack.optimize.OccurenceOrderPlugin(true) # preferEntry true
        # new webpack.optimize.DedupePlugin()
        # new webpack.optimize.UglifyJsPlugin()
        new ExtractTextPlugin('[name]-[hash].css')
        # getting placed below where it's needed in
        # new webpack.optimize.CommonsChunkPlugin("commons.chunk-[hash].js")
        # new webpack.SourceMapDevToolPlugin(
        #   "map/bundle.[hash].js.map",
        #   "\n//# sourceMappingURL=http://127.0.0.1:8000/webpack/[url]"
        # )
    ]
