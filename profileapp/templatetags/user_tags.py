from django import template

register = template.Library()

@register.tag(name="edit_list")
def do_edit_user(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, user = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    return EditUserNode (user)


class EditUserNode(template.Node):
    def __init__ (self, user):
        self.user = user

    def render (self, context):
        return 'I <b>am</b> a link for %s'%context[self.user].get_profile().last_name