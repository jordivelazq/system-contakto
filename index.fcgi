#!/opt/python27/bin/python
import sys, os, user

# Add a custom Python path. (optional)
sys.path.insert(0, "/var/www/vhosts/contaktoapp.com/httpdocs")

# Switch to the directory of your project.
os.chdir("/var/www/vhosts/contaktoapp.com/httpdocs")

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "contakto.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
