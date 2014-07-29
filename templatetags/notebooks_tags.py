from django import template

register = template.Library()


class NotebookNode(template.Node):
    def __init__(self, app_label, model):
        self.app_label = app_label
        self.model = model

    def render(self, context):
        t = template.loader.get_template('notebooks/notebook.html')
        return t.render(template.Context(
            {'app_label': self.app_label, 'model': self.model},
            autoescape=context.autoescape))

@register.tag
def notebook(parser, token):
    """
    Display the notebooks for an app and a model

    Syntax::

        {% notebook app_label model %}

    Examples::

        {% notebook "catalog" "product" %}
    """

    bits = token.split_contents()
    syntax_message = ("%(tag_name)s expects a syntax of %(tag_name)s "
                      "'app_label' 'model'" %
                      dict(tag_name=bits[0]))

    if len(bits) != 3:
        raise template.TemplateSyntaxError(syntax_message)

    app_label = bits[1]
    if not (app_label[0] == app_label[-1] and app_label[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % bits[0])

    model = bits[2]
    if not (model[0] == model[-1] and model[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % bits[0])

    return NotebookNode(app_label=app_label[1:-1], model=model[1:-1])

