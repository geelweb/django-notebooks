from django.shortcuts import render_to_response
from django.template import RequestContext
from ads.models import Ad

def notebook(request):
    return render_to_response('notebooks/notebook.html',
                              context_instance=RequestContext(request))

def item(request):
    pk = request.GET['pk']
    ad = Ad.objects.get(pk=pk)

    return render_to_response('notebooks/item.html',
                              {'ad': ad},
                              context_instance=RequestContext(request))
