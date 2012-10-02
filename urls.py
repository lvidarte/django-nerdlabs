import os.path

from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # =============
    # Static server
    # =============
    url(r'^media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT},
        name='blog-media'
    ),
    url(r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT},
        name='blog-static'
    ),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^pages/', include('django.contrib.flatpages.urls')),
    (r'^blog/', include('calcifer.blog.urls')),
    (r'^cache/', include('calcifer.cache.urls')),
    (r'^snippets/', include('calcifer.snippets.urls')),

)

