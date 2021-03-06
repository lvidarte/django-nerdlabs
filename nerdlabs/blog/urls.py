"""
Author: Leo Vidarte <http://nerdlabs.com.ar>

This is free software,
you can redistribute it and/or modify it
under the terms of the GPL version 3
as published by the Free Software Foundation.

"""

from django.conf.urls import patterns, url, include

from nerdlabs.blog.feeds import PostFeed
from nerdlabs.blog.models import Post


urlpatterns = patterns('nerdlabs.blog.views',

    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[-\w]+)/$',
        view='post_detail',
        name='blog-post-detail'
    ),

    (r'^archive/', 'post_archive', {}, 'blog-post-archive'),
    (r'^feeds/$', PostFeed(), {}, 'blog-feeds'),

    url(r'^search/$',
        view='post_search',
        name='blog-post-search'
    ),

    url(r'^tags/(?P<slug>[-\w]+)/$',
        view='post_list_by_tag',
        name='blog-post-list-by-tag'
    ),

    (r'^tags/', 'tag_cloud', {}, 'blog-tag-cloud'),

    url(r'^$', view='post_list', name='blog-post-list'),
)
