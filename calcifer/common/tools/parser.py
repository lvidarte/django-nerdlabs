# -*- coding: utf-8 -*-

import re


# Tag types
SHOW = 1 # [[label|200]]
LINK = 2 # {{label|text}}

# Markups
HTML = 1
REST = 2 # reStructuredText
TEXT = 3


def parse_media_tags(text, files, markup): # {{{
    """Parse media tags for easy insert of files into body text.

    Show tags:
        [[label_img]]                  show image
        [[label_img|size]]             show thumb
        [[label_img|size|target]]      show thumb + link to target
        [[label_pdf]]                  link to pdf
        [[label_pdf|text]]             link to pdf with text

    Link tags:
        {{label_img}}                  link to image
        {{label_file}}                 link to file
        {{label_file|text}}            link to file with text

    """

    # SHOW [[label]]
    for tag in re.findall('\[\[[^\]]+\]\]', text):
        ptag = parse_tag(tag, files, type=SHOW)
        if ptag:
            src = get_src(ptag, markup)
            if src:
                text = text.replace(tag, src)

    # LINK {{label}}
    for tag in re.findall('\{\{[^\}]+\}\}', text):
        ptag = parse_tag(tag, files, type=LINK)
        if ptag:
            src = get_src(ptag, markup)
            if src:
                text = text.replace(tag, src)

    return text
# }}}
def parse_tag(tag, files, type): # {{{
    _ = {
        'obj'      : None,
        'width'    : None,
        'text'     : None,
        'target'   : None,
        'css_class': None,
        'type'     : type
    }

    # Split tags into tokens
    if type == SHOW:
        tokens = tag.strip('[] ').split('|')
        _['css_class'] = get_css_class(tag)
    elif type == LINK:
        tokens = tag.strip('{} ').split('|')
        _['css_class'] = None
    else:
        return None

    # Avoid empty tags
    lent = len(tokens)
    if lent < 1:
        return None

    # Get object which is pointed by label
    _['obj'] = get_object(files, tokens[0])
    if not _['obj']:
        return None

    # Images
    if _['obj'].file.is_image:
        # Analysis second token
        if lent > 1:
            # Width
            if tokens[1].isdigit() and type==SHOW:
                _['width'] = tokens[1]
            # Just a link
            elif type == LINK:
                _['text'] = tokens[1]
            # Tag "show" image that becomes "link"
            elif type == SHOW:
                _['text'] = tokens[1]
                _['type'] = LINK
            # Not implemented
            else:
                return None
        # Analysis third token
        if lent > 2:
            if type == SHOW:
                _['target'] = get_object(files, tokens[2])
                if not _['target']:
                    return None
            # Not implemented
            else:
                return None
    # Others
    else:
        # Analysis second token (only text is allowed)
        if lent > 1:
            _['text'] = tokens[1]

    return _
# }}}
def get_css_class(tag): # {{{
    # Image align
    if tag[2] == ' ' and tag[-3] == ' ':
        return "align-center"
    elif tag[2] == ' ':
        return "align-right"
    elif tag[-3] == ' ':
        return "align-left"
    else:
        return "align-none"
# }}}
def get_object(files, label): # {{{
    try:
        object = files.through.objects.get(label=label)
    except:
        object = None
    return object
# }}}
def get_src(ptag, markup): # {{{
     # {{{ Thumb with link to file
    if ptag['target']:
        if markup == HTML:
            return u''.join((
                     '<a href="%s" title="%s">',
                     '<img src="%s" alt="%s" class="%s" />',
                     '</a>')) % (
                        ptag['target'].file.get_absolute_url(),
                        ptag['target'].description,
                        ptag['obj'].file.get_url_wthumb(ptag['width']),
                        ptag['obj'].file.alt,
                        ptag['css_class']) 
        elif markup == REST:
            return u'\n'.join((
                    '.. image:: %s',
                    '   :alt: %s',
                    '   :target: %s',
                    '   :class: %s')) % (
                        ptag['obj'].file.get_url_wthumb(width=ptag['width']),
                        ptag['obj'].file.alt,
                        ptag['target'].file.get_absolute_url(),
                        ptag['css_class'])
        elif markup == TEXT:
            return ptag['obj'].file.get_absolute_url()
    # }}}
    # {{{ Thumb
    elif ptag['width']:
        if markup == HTML:
            return u'<img src ="%s" alt="%s" class="%s" />' % (
                        ptag['obj'].file.get_url_wthumb(ptag['width']),
                        ptag['obj'].file.alt,
                        ptag['css_class']) 
        elif markup == REST:
            return u'\n'.join((
                    '.. image:: %s',
                    '   :alt: %s',
                    '   :class: %s')) % (
                        ptag['obj'].file.get_url_wthumb(width=ptag['width']),
                        ptag['obj'].file.alt,
                        ptag['css_class'])
        elif markup == TEXT:
            return ptag['obj'].file.get_url_wthumb(width=ptag['width'])
    # }}}
    # {{{ Link with text
    elif ptag['text']:
        if markup == HTML:
            return u'<a href="%s" title="%s">%s</a>' % (
                        ptag['obj'].file.get_absolute_url(),
                        ptag['obj'].description,
                        ptag['text']) 
        elif markup == REST:
            return u'`%s <%s>`_' % (
                        ptag['text'],
                        ptag['obj'].file.get_absolute_url())
        elif markup == TEXT:
            return u'%s <%s>' % (
                        ptag['text'],
                        ptag['obj'].file.get_absolute_url())
    # }}}
    # {{{ Image
    elif ptag['obj'].file.is_image and ptag['type'] == SHOW:
        if markup == HTML:
            return u'<img src="%s" alt="%s" class="%s" />' % (
                        ptag['obj'].file.get_absolute_url(),
                        ptag['obj'].file.alt,
                        ptag['css_class']) 
        elif markup == REST:
            return u'\n'.join((
                    '.. image:: %s',
                    '   :alt: %s',
                    '   :class: %s')) % (
                        ptag['obj'].file.get_absolute_url(),
                        ptag['obj'].file.alt,
                        ptag['css_class'])
        elif markup == TEXT:
            return ptag['obj'].file.get_absolute_url()
    # }}}
    # {{{ Link
    else:
        if markup == HTML:
            return u'<a href="%s" title="%s">%s</a>' % (
                        ptag['obj'].file.get_absolute_url(),
                        ptag['obj'].description,
                        ptag['obj'].file.get_absolute_url()) 
        elif markup == REST:
            return u'`%s <%s>`_' % (
                        ptag['obj'].file.get_absolute_url(),
                        ptag['obj'].file.get_absolute_url())
        elif markup == TEXT:
            return ptag['obj'].file.get_absolute_url()
    # }}}
    return None
# }}}
def rest_to_html(rest_src): # {{{
    try:
        from  docutils import core
    except ImportError:
        raise Exception("Docutils is not installed.")
    parts = core.publish_parts(source=rest_src, writer_name='html')
    return parts['body_pre_docinfo'] + parts['fragment']
# }}}
def text_to_html(text_src): # {{{
    return text_src.replace('\n', '<br />')
# }}}
def parse_tag_more(src, stop=False, link='', text_link='more'): # {{{
    if stop and link:
        i = src.find('[:more:]')
        if i >= 0:
            src = src[:i] + u"""<p class="read-more">
                                <a href="%s#more" title="">%s</a> »
                                </p>""" % (link, text_link)
    else:
        src = src.replace(u'[:more:]', u'<a id="more"></a>')
    return src
# }}}

