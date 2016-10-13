# -*- coding: utf-8 -*-

"""
Author: Leo Vidarte <http://nerdlabs.com.ar>

This is free software,
you can redistribute it and/or modify it
under the terms of the GPL version 3
as published by the Free Software Foundation.

"""

from django.conf import settings
from django.core.cache import cache


class NginxMemcacheMiddleWare:
    def process_response(self, request, response):
        path = request.get_full_path()

        if getattr(settings, 'BLOG_CACHE_ENABLED', False) \
           and request.method == "GET" \
           and response.status_code == 200:

            key = "blog:%s" % path
            timeout = getattr(settings, 'BLOG_CACHE_TIMEOUT', 3600)

            cache.set(key, response.content, timeout)

        return response

