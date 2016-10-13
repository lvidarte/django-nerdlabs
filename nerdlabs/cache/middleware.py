# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.cache import cache


class NginxMemcacheMiddleware:
    def process_response(self, request, response):
        path = request.get_full_path()

        if getattr(settings, 'CACHE_ENABLED', False) \
           and request.method == "GET" \
           and response.status_code == 200 \
           and not request.user.is_authenticated():

            #from nerdlabs.cache import make_key
            #from datetime import datetime
            #key = make_key(path, 'nerdlabs', '')
            #action = "found" if cache.get(key) else "not found"
            #f = open('/tmp/cache.log', 'a')
            #f.write("[%s] %s: %s\n" % (datetime.now(), action, key))

            cache.set(path, response.content)

        return response


