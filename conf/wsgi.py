"""
WSGI config for quipu project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""
import os
from pathlib import Path
import sys

from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings.development')

current_path = Path(__file__).resolve()
sys.path.append(Path(current_path.parent))
sys.path.append(Path(current_path.parent.parent, 'quipu'))

application = get_wsgi_application()
