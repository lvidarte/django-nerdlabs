from django.conf.urls import patterns, url, include
from django.views.generic.list_detail import object_list
from django.views.generic.list_detail import object_detail
from calcifer.snippets.models import *


snippet_info = {'queryset': Snippet.objects.all()}

urlpatterns = patterns('',
    (r'^$', object_list,
        dict(snippet_info, paginate_by=20),
        'calcifer-snippet-list'),
    (r'^(?P<object_id>\d+)/$', object_detail,
        snippet_info, 'calcifer-snippet-detail'),
)

