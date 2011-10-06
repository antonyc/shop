#!/usr/bin/env python
from django.core.management import execute_manager
import os
import sys
import imp
if os.path.exists('/etc/amadika/shop'):
    sys.path.append('/etc/amadika/shop')
 
try:
    imp.find_module('settings') # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)

import settings

if __name__ == "__main__":
    execute_manager(settings)
