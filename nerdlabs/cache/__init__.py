"""
Author: Leo Vidarte <http://nerdlabs.com.ar>

This is free software,
you can redistribute it and/or modify it
under the terms of the GPL version 3
as published by the Free Software Foundation.

"""

from django.utils.encoding import smart_str

def make_key(key, key_prefix, version):
    return ':'.join([key_prefix, smart_str(key)])
