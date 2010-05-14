from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.tag(name="edit_list")
def do_edit_user(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, user = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, \
                "%r tag requires a single argument" % token.contents.split()[0]
    return EditUserNode (user)


class EditUserNode(template.Node):
    def __init__ (self, user):
        self.user = user
        super(template.Node, self).__init__()

    def render (self, context):
        try:
            return '<a href="%s">Edit profile for %s %s</a>'% (
                    reverse('edit_profile',kwargs={'user':context[self.user]}),
                    context[self.user].get_profile().first_name,
                    context[self.user].get_profile().last_name
                    )
        except (ValueError, KeyError):
            return ""