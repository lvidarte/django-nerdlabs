"""
Author: Leo Vidarte <http://nerdlabs.com.ar>

This is free software,
you can redistribute it and/or modify it
under the terms of the GPL version 3
as published by the Free Software Foundation.

"""

from django.conf.urls import patterns, url, include
from nerdlabs.cache.views import *

# patterns(prefix, pattern_description, ...)
# 
# pattern_description:
# (regular expression, Python callback function [, dictionary [, name]])


urlpatterns = patterns('nerdlabs.cache.views',

    (r'^styles/([a-zA-Z_]+)\.css', parse_dcss_file),

    url(r'^imgs/w/(?P<width>\d{2,3})(?P<url>/.+)$',
        view='img_resize',
        name='cache-imgs-w'
    ),

    url(r'^imgs/h/(?P<height>\d{2,3})(?P<url>/.+)$',
        view='img_resize',
        name='cache-imgs-h'
    ),

    (r'^rm(/[-0-9a-zA-Z_/\.]+)$', cache_rm),

    (r'^status', memcached_status),

)
