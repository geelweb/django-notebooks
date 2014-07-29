from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django import template
from django.core import serializers
from notebooks.models import NotebookItem


def item(request, app_label, model):
    pk = request.GET['pk']

    content_type = ContentType.objects.get(app_label=app_label, model=model)
    item = content_type.get_object_for_this_type(pk=pk)

    t = template.loader.select_template([
        '%s/notebooks/item.html' % app_label,
        'notebooks/item.html',
    ])


    return HttpResponse(t.render(template.RequestContext(request, {'item': item})))

def store(request, app_label, model, pk):
    if request.user.is_authenticated():
        content_type = ContentType.objects.get(app_label=app_label, model=model)
        NotebookItem.objects.get_or_create(user=request.user, content_type=content_type, object_id=pk)
    return HttpResponse()

def load(request, app_label, model):
    if request.user.is_authenticated():
        content_type = ContentType.objects.get(app_label=app_label, model=model)
        collection = NotebookItem.objects.filter(user=request.user, content_type=content_type)
        return HttpResponse(
                serializers.serialize("json", collection),
                content_type='application/json')
    return HttpResponse('[]', content_type='application/json')
