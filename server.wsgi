import os
import sys

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                           os.path.pardir))

sys.path.append(APP_ROOT)
#os.chdir(APP_ROOT)

os.environ['DJANGO_SETTINGS_MODULE'] = 'calcifer.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
