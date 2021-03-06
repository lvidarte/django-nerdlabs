# -*- coding: utf-8 -*-

"""
Author: Leo Vidarte <http://nerdlabs.com.ar>

This is free software,
you can redistribute it and/or modify it
under the terms of the GPL version 3
as published by the Free Software Foundation.

"""

from django.conf import settings
from django.contrib.syndication.views import Feed
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from nerdlabs.blog.models import Post


class PostFeed(Feed):
    _site = Site.objects.get_current()
    title = settings.BLOG_NAME
    description = settings.BLOG_DESCRIPTION

    def link(self):
        return reverse('blog-post-list')

    def items(self):
        return Post.published.all()[:10]

    def item_pubdate(self, item):
        return item.publish

    def item_author_name(self, item):
        return '%s' % (item.author)

    def item_description(self, item):
        return item.get_body_html()
