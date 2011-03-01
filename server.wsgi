import os
import sys

APP_ROOT = os.path.abspath(os.path.dirname(__file__))

sys.path.append(APP_ROOT)

#open('/tmp/path.txt', 'w').write("\n".join(sys.path))
#os.chdir(APP_ROOT)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
