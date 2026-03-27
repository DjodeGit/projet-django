"""
WSGI config for mon_projet project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')

# Exécuter les migrations et créer le superuser au démarrage
from django.core.management import execute_from_command_line

# Migrate first
execute_from_command_line(['manage.py', 'migrate', '--noinput'])

# Then create superuser if needed
execute_from_command_line(['manage.py', 'create_superuser'])

application = get_wsgi_application()
