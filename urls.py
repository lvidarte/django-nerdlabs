import os.path

from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^pages/', include('django.contrib.flatpages.urls')),
    (r'^blog/', include('calcifer.blog.urls')),
    (r'^cache/', include('calcifer.cache.urls')),
    (r'^snippets/', include('calcifer.snippets.urls')),

    (r'^favicon.ico$', 'django.views.generic.simple.redirect_to',
                      {'url': '/static/favicon.ico'}),
    (r'^robots.txt$', 'django.views.generic.simple.redirect_to',
                      {'url': '/static/robots.txt'}),

    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/blog/'}),

)


if getattr(settings, 'STATIC_SERVER', False):
    urlpatterns += patterns('',
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
    )


