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


class AddToNotebookNode(template.Node):
    def __init__(self, app_label, model, object_id):
        self.app_label = app_label
        self.model = model
        self.object_id = template.Variable(object_id)

    def render(self, context):
        t = template.loader.get_template('notebooks/add_to_notebook_btn.html')
        return t.render(template.Context({
            'app_label': self.app_label,
            'model': self.model,
            'object_id': self.object_id.resolve(context),
            }, autoescape=context.autoescape))

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

@register.tag
def add_to_notebook(parser, token):
    """
    Display the button to add an item to the notebook

    Syntax::

        {% notebook "app_label" "model" object_id %}

    Example::

        {% notebook "catalog" "product" product.pk %}
    """

    bits = token.split_contents()
    syntax_message = ("%(tag_name)s expects a syntax of %(tag_name)s "
                      "'app_label' 'model' object_id" %
                      dict(tag_name=bits[0]))

    if len(bits) != 4:
        raise template.TemplateSyntaxError(syntax_message)

    app_label = bits[1]
    if not (app_label[0] == app_label[-1] and app_label[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % bits[0])

    model = bits[2]
    if not (model[0] == model[-1] and model[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % bits[0])

    object_id = bits[3]

    return AddToNotebookNode(app_label=app_label[1:-1], model=model[1:-1], object_id=object_id)
