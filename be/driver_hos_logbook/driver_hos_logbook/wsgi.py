"""
WSGI config for driver_hos_logbook project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
# from django.core.management import call_command
_driver_hos_logbook_environment = os.environ.get("DRIVER_HOS_LOGBOOK_ENVIRONMENT")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'driver_hos_logbook.settings')
os.environ.setdefault("DJANGO_CONFIGURATION", _driver_hos_logbook_environment.capitalize() if _driver_hos_logbook_environment else "Prod")

from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()
