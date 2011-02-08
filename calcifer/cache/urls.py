from django.conf.urls.defaults import *
from calcifer.cache.views import parse_dcss_file, img_resize

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

)
