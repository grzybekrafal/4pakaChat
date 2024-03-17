import os,sys
virtenv = os.path.expanduser('~') + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
   if sys.version.split(' ')[0].split('.')[0] == '3':
       exec(compile(open(virtualenv, "rb").read(), virtualenv, 'exec'), dict(__file__=virtualenv))
   else:
       execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
   pass

sys.path.append(os.path.expanduser('~'))


os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

import time
import traceback
import signal
from django.core.wsgi import get_wsgi_application

try:
    application = get_wsgi_application()
except Exception:
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)
