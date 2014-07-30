from django.conf.urls import patterns, url

urlpatterns = patterns('geelweb.django.notebooks.views',
    url(r'^(?P<app_label>[-_\w]+)/(?P<model>[-_\w]+)/item/$', 'item', name="notebook_item"),
    url(r'^(?P<app_label>[-_\w]+)/(?P<model>[-_\w]+)/store/(?P<pk>\d+)/$', 'store', name="notebook_store"),
    url(r'^(?P<app_label>[-_\w]+)/(?P<model>[-_\w]+)/load/$', 'load', name="notebook_load"),
)

