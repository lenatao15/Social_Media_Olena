"""
WSGI config for FeedProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FeedProject.settings')

application = get_wsgi_application()

try:
    print("Auto-running database migrations...")
    call_command('migrate', no_input=True)
    print("Database migrations applied successfully.")
except Exception as e:
    print(f"Error auto-running migrations: {e}")

