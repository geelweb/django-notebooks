from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django import template

def notebook(request):
    return render_to_response('notebooks/notebook.html',
                              context_instance=RequestContext(request))

def item(request, app_label, model):
    pk = request.GET['pk']

    content_type = ContentType.objects.get(app_label=app_label, model=model)
    item = content_type.get_object_for_this_type(pk=pk)

    t = template.loader.select_template([
        '%s/notebooks/item.html' % app_label,
        'notebooks/item.html',
    ])


    return HttpResponse(t.render(template.RequestContext(request, {'item': item})))
