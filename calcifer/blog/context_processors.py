from django.conf import settings

def blog(request):
    return {
        'BLOG_NAME': getattr(settings, 'BLOG_NAME', u'calcifer'),
        'BLOG_DESCRIPTION': getattr(settings,
                                    'BLOG_DESCRIPTION',
                                    u'A minimalist blog'),
        'DATE_FORMAT': getattr(settings, 'DATE_FORMAT', 'F j, Y'),
        'DATETIME_FORMAT': getattr(settings,
                                   'DATETIME_FORMAT',
                                   'F j, Y H:i:s'),
    }
