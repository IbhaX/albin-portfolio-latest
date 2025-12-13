"""
WSGI config for ibhax project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ibhax.settings')

application = get_wsgi_application()
