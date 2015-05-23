nib = require 'nib'
path = require 'path'
webpack = require 'webpack'
ExtractTextPlugin = require 'extract-text-webpack-plugin'
BundleTracker = require 'webpack-bundle-tracker'

module.exports =
    context: __dirname
    entry: './js/main.coffee'
    output:
        path: './bundles/'
        filename: '[name]-[hash].js'
        chunkFilename: '[id].js'
    module:
        loaders: [
            {test: /\.coffee$/, loader: 'coffee-loader'}
            {test: /\.(coffee\.md|litcoffee)$/, loader: "coffee-loader?literate"}
            # {test: /\.styl$/, loader: 'style-loader!css-loader!stylus-loader'}
            {test: /\.styl$/, loader: ExtractTextPlugin.extract('style-loader', 'css-loader?sourceMap!stylus-loader')}
            {test: /\.less$/, loader: ExtractTextPlugin.extract('style-loader', 'css-loader!less-loader')}
            {test: /\.css$/, loader: ExtractTextPlugin.extract('style-loader', 'css-loader')}
        ]
    resolve:
        root: __dirname
        # root: [ path.join(root, 'node_modules') ]
        modulesDirectories: ['../node_modules',]
        # hangs when uncommented
        # extensions: ['', '.js', '.styl', '.coffee', '.coffee.md', '.litcoffee', '.css']
    # Stylus loader options
    stylus:
        use: [nib()]
        import: ['variables', 'mixins']
    devtool: 'sourcemap'

    plugins: [
        new BundleTracker()
        new webpack.optimize.OccurenceOrderPlugin(true) # preferEntry true
        # new webpack.optimize.DedupePlugin()
        # new webpack.optimize.UglifyJsPlugin()
        new ExtractTextPlugin('[name]-[hash].css', allChunks: true)
        # new webpack.optimize.CommonsChunkPlugin("commons.chunk-[hash].js")
    ]
