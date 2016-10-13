import os.path

from django.conf.urls import patterns, url, include
from django.conf import settings
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^pages/', include('django.contrib.flatpages.urls')),
    (r'^blog/', include('nerdlabs.blog.urls')),
    (r'^cache/', include('nerdlabs.cache.urls')),

    (r'^favicon.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    (r'^robots.txt$', RedirectView.as_view(url='/static/robots.txt')),

    (r'^$', RedirectView.as_view(url='/blog/')),

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


