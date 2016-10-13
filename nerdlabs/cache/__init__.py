from django.utils.encoding import smart_str

def make_key(key, key_prefix, version):
    return ':'.join([key_prefix, smart_str(key)])
