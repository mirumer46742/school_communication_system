import os
import sys
import site

activate_this = '/srv/envs/env_scs/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
sys.path.append('/srv/www/school_communication_system')
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
site.addsitedir('/srv/envs/env_scs/lib/python2.7/site-packages')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
