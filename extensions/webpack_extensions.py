from jinja2.ext import Extension

from webpack.compiler import webpack


def webpack_bundler(config=None):
    return webpack(config)


class WebpackExtensions(Extension):
    def __init__(self, environment):
        super(WebpackExtensions, self).__init__(environment)
        environment.globals["webpack_bundler"] = webpack_bundler
