# from __future__ import unicode_literals

from jinja2.ext import Extension

# patch shit
from mezzanine import template
prev_as_tag = template.Library.as_tag
template.Library.as_tag = lambda lib, func: func

from mezzanine.core.templatetags import mezzanine_tags
from mezzanine.generic.templatetags.keyword_tags import keywords_for

# kick it along
template.Library.as_tag = prev_as_tag


class MezzanineFilterExtension(Extension):
    def __init__(self, environment):
        super(MezzanineFilterExtension, self).__init__(environment)
        environment.globals["is_installed"] = mezzanine_tags.is_installed
        environment.filters["richtext_filters"] = mezzanine_tags.richtext_filters
        environment.globals["keywords_for"] = keywords_for
