# -*- coding: utf-8 -*-
import os.path
import Image, ImageDraw
import math
import datetime

from django.http import HttpResponse
from django.http import Http404
from django.conf import settings

from calcifer.common.tools import clevercss


def parse_dcss_file(request, filename): # {{{
    # http://github.com/timparkin/clevercss
    # http://lucumr.pocoo.org/2007/9/17/using-clevercss-in-django
    fn = os.path.join(settings.PROJECT_PATH,
                      'calcifer/blog/styles', '%s.dcss' % filename)
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

        return HttpResponse(css, mimetype='text/css')
    finally:
        f.close()
# }}}
def img_resize(request, url, width=0, height=0): # {{{
    try:
        image = Image.open(settings.MEDIA_ROOT + url)
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
            response = HttpResponse(mimetype="image/%s"%image.format)
            image.save(response, image.format, quality=90)
            return response
        else:
            raise Http404()
# }}}

