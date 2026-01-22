#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from configurations import importer

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'driver_hos_logbook.settings')
    environment = os.environ.get("DRIVER_HOS_LOGBOOK_ENVIRONMENT", "dev").capitalize()
    os.environ.setdefault("DJANGO_CONFIGURATION", environment)
    
    try:
        from configurations.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    importer.install()
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
