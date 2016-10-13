"""
Author: Leo Vidarte <http://nerdlabs.com.ar>

This is free software,
you can redistribute it and/or modify it
under the terms of the GPL version 3
as published by the Free Software Foundation.

"""

from django import template

register = template.Library()

## ver reverse()


@register.filter
def wthumb(value, size):
    return "/cache/imgs/w/%s%s" % (size, value)


@register.filter
def hthumb(value, size):
    return "/cache/imgs/h/%s%s" % (size, value)

