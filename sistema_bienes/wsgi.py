import os
from django.core.wsgi import get_wsgi_application
from decouple import config

environment = config('DJANGO_ENV', default='production')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'sistema_bienes.settings.{environment}')

application = get_wsgi_application()