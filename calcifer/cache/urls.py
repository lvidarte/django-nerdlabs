from django.conf.urls.defaults import *
from calcifer.cache.views import *

# patterns(prefix, pattern_description, ...)
# 
# pattern_description:
# (regular expression, Python callback function [, dictionary [, name]])


urlpatterns = patterns('calcifer.cache.views',

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
