""" Module for {% edit_list user %} tag"""
from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.tag(name="edit_list")
def do_edit_user(parser, token):
    """ the tag {% edit_list user %} generates a link to edit user's profile
    if user variable is invalid, it outputs empty string
    """
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, user = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, \
                "%r tag requires a single argument" % token.contents.split()[0]
    return EditUserNode (user)


class EditUserNode(template.Node):
    """ This node is used to render user_list tag"""
    def __init__ (self, user):
        self.user = user
        template.Node.__init__(self)

    def render (self, context):
        try:
            return '<a href="%s">Edit profile for %s %s</a>'% (
                    reverse('edit_profile',kwargs={'user':context[self.user]}),
                    context[self.user].get_profile().first_name,
                    context[self.user].get_profile().last_name
                    )
        except (ValueError, KeyError):
            return ""