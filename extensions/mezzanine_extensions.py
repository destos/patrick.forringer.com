# from __future__ import unicode_literals

from jinja2.ext import Extension

from mezzanine.core.templatetags import mezzanine_tags


class MezzanineFilterExtension(Extension):
    def __init__(self, environment):
        super(MezzanineFilterExtension, self).__init__(environment)
        environment.globals["is_installed"] = mezzanine_tags.is_installed
