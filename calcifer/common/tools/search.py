# -*- coding: utf-8 -*-


from stop_words import STOP_WORDS
def strip_stop_words(text):
    return [w for w in text.split() if strip_diacritics(w) not in STOP_WORDS]


from unicodedata import normalize, category
def strip_diacritics(word):
    return ''.join(
        [c for c in normalize('NFD', word) if category(c) == 'Ll'])


from django.db.models import Q
def get_q(words_list, field_name, op='and'):
    if op not in ('and', 'or'):
        raise Exception("op must be 'and' or 'or'")
    r = None
    for w in words_list:
        q = Q(**{field_name + '__icontains': w})
        if r:
            r = r & q if op == 'and' else r | q
        else:
            r = q
    return r
