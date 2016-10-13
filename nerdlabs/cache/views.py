# -*- coding: utf-8 -*-

import os.path
from PIL import Image, ImageDraw
import math
import datetime, re

from django.conf import settings
from django.http import HttpResponse
from django.http import Http404
from django.core.cache import cache
from django.shortcuts import render_to_response

from nerdlabs.common.tools import clevercss


def parse_dcss_file(request, filename):
    # http://github.com/timparkin/clevercss
    # http://lucumr.pocoo.org/2007/9/17/using-clevercss-in-django
    fn = os.path.join(settings.STATIC_ROOT, 'dcss', '%s.dcss' % filename)
    if not os.path.exists(fn):
        raise Http404()
    f = file(fn)
    try:
        css = "/* %s */\n\n" % datetime.datetime.now()
        css += clevercss.convert(f.read().decode('utf-8'))

        if not settings.DEBUG:
            l = []
            for line in css.split('\n'):
                if not line:
                    l.append('\n')
                l.append(line.strip())

            compress = ''.join(l)
            compress = compress.replace(': ', ':')

            # comentar las 3 lineas siguientes para
            # mayor compresion y menor legibilidad
            compress = compress.replace(';', '; ')
            compress = compress.replace('{', '{ ')
            compress = compress.replace(',', ', ')

            css = compress

        return HttpResponse(css, content_type='text/css')
    finally:
        f.close()


def img_resize(request, url, width=0, height=0):
    try:
        url_ = url[len('media/')+1:] # strip 'media/'
        image = Image.open(settings.MEDIA_ROOT + url_)
    except:
        raise Http404()
    else:
        w, h = image.size
        width = int(width)
        height = int(height)

        if width and \
           width in getattr(settings, 'IMG_ALLOWED_WIDTHS', (width,)):
            height = int(math.ceil(float(width) * float(h) / float(w)))
        elif height and \
             height in getattr(settings, 'IMG_ALLOWED_HEIGHTS', (height,)):
            width = int(math.ceil(float(height) * float(w) / float(h)))

        if width and height:
            image.thumbnail((width, height), Image.ANTIALIAS)
            draw = ImageDraw.Draw(image)
            #draw.text((5,5), "%dx%d" % (width, height))
            #draw.text((5,5), datetime.now().strftime('%H:%M:%S'))
            response = HttpResponse(content_type="image/%s"%image.format)
            image.save(response, image.format, quality=90)
            return response
        else:
            raise Http404()


def cache_rm(request, path):
    # http://djangosnippets.org/snippets/936/
    if cache.has_key(path):
        cache.delete(path)
        result = "DELETED"
    else:
        result = "NOT FOUND"
    return HttpResponse('<h1>%s</h1><h4>%s</h4>' % (result, path))


def memcached_status(request):
    # http://effbot.org/zone/django-memcached-view.htm
    try:
        import memcache
    except ImportError:
        raise Http404

    #if not (request.user.is_authenticated() and
    #        request.user.is_staff):
    #    raise Http404

    # get first memcached URI
    m = re.match(
        "([.\w]+:\d+)", settings.CACHES['default']['LOCATION'])
    if not m:
        raise Http404

    host = memcache._Host(m.group(1))
    host.connect()
    host.send_cmd("stats")

    class Stats:
        pass

    stats = Stats()

    while 1:
        line = host.readline().split(None, 2)
        if line[0] == "END":
            break
        stat, key, value = line
        try:
            # convert to native type, if possible
            value = int(value)
            if key == "uptime":
                value = datetime.timedelta(seconds=value)
            elif key == "time":
                value = datetime.datetime.fromtimestamp(value)
        except ValueError:
            pass
        setattr(stats, key, value)

    host.close_socket()

    try:
        hit_rate = 100 * stats.get_hits / stats.cmd_get
    except:
        hit_rate = 0

    return render_to_response(
        'cache/memcache_status.html', dict(
            stats=stats,
            hit_rate=hit_rate,
            time=datetime.datetime.now(), # server time
    ))


