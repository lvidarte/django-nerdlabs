# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.cache import cache


class NginxMemcacheMiddleware: # {{{
    def process_response(self, request, response):
        path = request.get_full_path()

        if getattr(settings, 'CACHE_ENABLED', False) \
           and request.method == "GET" \
           and response.status_code == 200:

            #key = getattr(settings, 'CALCIFER_CACHE_KEY', '') + path
            key = path
            timeout = 60*3 #getattr(settings, 'CACHE_TIMEOUT', 3600)

            from datetime import datetime
            action = "found" if cache.get(key) else "not found"
            open('/tmp/cache.log', 'a').write("[%s] %s: %s\n" % (datetime.now(), action, key))

            cache.set(path, response.content, timeout)

        return response
# }}}

