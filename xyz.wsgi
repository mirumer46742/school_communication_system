import os
import sys
import site

activate_this = '/home/mirumer/Applied/ENV/env_django/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
sys.path.append('/home/mirumer/Applied/landingpagesystem')
os.environ['DJANGO_SETTINGS_MODULE'] = 'landingpage.settings_umer'
site.addsitedir('/home/mirumer/Applied/ENV/env_django/lib/python2.7/site-packages')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()