from django.conf.urls.defaults import *
#from django.views.generic.simple import direct_to_template

from calcifer.blog.feeds import PostFeed

# patterns(prefix, pattern_description, ...)
# 
# pattern_description:
# (regular expression, Python callback function [, dictionary [, name]])


urlpatterns = patterns('calcifer.blog.views',

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        view='post_detail',
        name='blog-post-detail'
    ),

    #(r'^about/', direct_to_template, {'template': 'blog/about.html'}),
    (r'^archive/', 'post_archive', {}, 'blog-post-archive'),
    (r'^tags/', 'tag_cloud', {}, 'blog-tag-cloud'),
    (r'^feeds/$', PostFeed(), {}, 'blog-feeds'),

    url(r'^search/$',
        view='post_search',
        name='blog-post-search'
    ),

    url(r'^tags/(?P<slug>[-\w]+)/$',
        view='post_list_by_tag',
        name='blog-post-list-by-tag'
    ),

    url(r'^$',
        view='post_list',
        name='blog-post-list'
    ),
)
