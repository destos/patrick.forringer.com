from __future__ import unicode_literals

from collections import defaultdict

from django.template import Context
from django.template.loader import get_template
import jinja2

# patch shit
from mezzanine import template
prev_as_tag = template.Library.as_tag
prev_render_tag = template.Library.render_tag
template.Library.as_tag = lambda lib, func: func
# template.Library.render_tag = lambda lib, func: func

from mezzanine.core.templatetags import mezzanine_tags
from mezzanine.generic.templatetags.keyword_tags import keywords_for
# no need to patch these modules
from mezzanine.pages.models import Page
from mezzanine.utils.urls import home_slug
# from mezzanine.pages.templatetags.pages_tags import page_menu

# kick it along
template.Library.as_tag = prev_as_tag
# template.Library.render_tag = prev_render_tag


# @jinja2.contextfunction
# def new_page_menu(context, *args, **kwargs):
#     token = ()
#     token.split_contents = lambda : [None, args[0]]
#     import ipdb; ipdb.set_trace()
#     return page_menu(context, token)


@jinja2.contextfunction
def new_page_menu(context, *args, **kwargs):
    # import ipdb; ipdb.set_trace()
    context = dict(context)
    template_name = None
    parent_page = None
    for part in args:
        if isinstance(part, str):
            template_name = part
        elif isinstance(part, Page):
            parent_page = part
    if template_name is None:
        try:
            template_name = context["menu_template_name"]
        except KeyError:
            error = "No template found for page_menu in: %s" % args
            raise jinja2.TemplateSyntaxError(error)
    context["menu_template_name"] = template_name
    if "menu_pages" not in context:
        try:
            user = context["request"].user
            slug = context["request"].path
        except KeyError:
            user = None
            slug = ""
        num_children = lambda id: lambda: len(context["menu_pages"][id])
        has_children = lambda id: lambda: num_children(id)() > 0
        rel = [m.__name__.lower() for m in Page.get_content_models()]
        published = Page.objects.published(for_user=user).select_related(*rel)
        # Store the current page being viewed in the context. Used
        # for comparisons in page.set_menu_helpers.
        if "page" not in context:
            try:
                context["_current_page"] = published.exclude(
                    content_model="link").get(slug=slug)
            except Page.DoesNotExist:
                context["_current_page"] = None
        elif slug:
            context["_current_page"] = context["page"]
        # Some homepage related context flags. on_home is just a helper
        # indicated we're on the homepage. has_home indicates an actual
        # page object exists for the homepage, which can be used to
        # determine whether or not to show a hard-coded homepage link
        # in the page menu.
        home = home_slug()
        context["on_home"] = slug == home
        context["has_home"] = False
        # Maintain a dict of page IDs -> parent IDs for fast
        # lookup in setting page.is_current_or_ascendant in
        # page.set_menu_helpers.
        context["_parent_page_ids"] = {}
        pages = defaultdict(list)
        for page in published.order_by("_order"):
            page.set_helpers(context)
            context["_parent_page_ids"][page.id] = page.parent_id
            setattr(page, "num_children", num_children(page.id))
            setattr(page, "has_children", has_children(page.id))
            pages[page.parent_id].append(page)
            if page.slug == home:
                context["has_home"] = True
        # Include menu_pages in all contexts, not only in the
        # block being rendered.
        context["menu_pages"] = pages
    # ``branch_level`` must be stored against each page so that the
    # calculation of it is correctly applied. This looks weird but if we do
    # the ``branch_level`` as a separate arg to the template tag with the
    # addition performed on it, the addition occurs each time the template
    # tag is called rather than once per level.
    context["branch_level"] = 0
    parent_page_id = None
    if parent_page is not None:
        context["branch_level"] = getattr(parent_page, "branch_level", 0) + 1
        parent_page_id = parent_page.id

    # Build the ``page_branch`` template variable, which is the list of
    # pages for the current parent. Here we also assign the attributes
    # to the page object that determines whether it belongs in the
    # current menu template being rendered.
    context["page_branch"] = context["menu_pages"].get(parent_page_id, [])
    context["page_branch_in_menu"] = False
    for page in context["page_branch"]:
        page.in_menu = page.in_menu_template(template_name)
        page.num_children_in_menu = 0
        if page.in_menu:
            context["page_branch_in_menu"] = True
        for child in context["menu_pages"].get(page.id, []):
            if child.in_menu_template(template_name):
                page.num_children_in_menu += 1
        page.has_children_in_menu = page.num_children_in_menu > 0
        page.branch_level = context["branch_level"]
        page.parent = parent_page
        context["parent_page"] = page.parent

        # Prior to pages having the ``in_menus`` field, pages had two
        # boolean fields ``in_navigation`` and ``in_footer`` for
        # controlling menu inclusion. Attributes and variables
        # simulating these are maintained here for backwards
        # compatibility in templates, but will be removed eventually.
        page.in_navigation = page.in_menu
        page.in_footer = not (not page.in_menu and "footer" in template_name)
        if page.in_navigation:
            context["page_branch_in_navigation"] = True
        if page.in_footer:
            context["page_branch_in_footer"] = True

    t = get_template(template_name)
    return jinja2.Markup(t.render(Context(context)))


class MezzanineExtension(jinja2.ext.Extension):
    """Mezzanine filters/tags/constants for Jinja"""

    def __init__(self, environment):
        super(MezzanineExtension, self).__init__(environment)
        environment.globals["is_installed"] = mezzanine_tags.is_installed
        environment.filters["richtext_filters"] = mezzanine_tags.richtext_filters
        environment.globals["keywords_for"] = keywords_for
        environment.globals["page_menu"] = new_page_menu
