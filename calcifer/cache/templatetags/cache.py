from django import template

register = template.Library()

## ver reverse()

@register.filter
def wthumb(value, size):
    return "/cache/imgs/w/%s%s" % (size, value)

@register.filter
def hthumb(value, size):
    return "/cache/imgs/h/%s%s" % (size, value)

