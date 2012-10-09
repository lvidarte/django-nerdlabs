from django.conf import settings

def blog(request):
    return {
        'BLOG_NAME': getattr(settings, 'BLOG_NAME', u''),
        'BLOG_DESCRIPTION': getattr(settings, 'BLOG_DESCRIPTION', u''),
        'BLOG_KEYWORDS': getattr(settings, 'BLOG_KEYWORDS', u''),
        'DATE_FORMAT': getattr(settings, 'DATE_FORMAT', 'F j, Y'),
        'DATETIME_FORMAT': getattr(settings, 'DATETIME_FORMAT', 'F j, Y H:i:s'),
        'GOOGLE_ANALYTICS_TEMPLATE': getattr(settings, 'GOOGLE_ANALYTICS_TEMPLATE', u''),
    }
