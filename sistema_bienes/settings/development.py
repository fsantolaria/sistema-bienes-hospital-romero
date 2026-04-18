from .base import *


DEBUG = True

import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///' + str(BASE_DIR / 'db_development.sqlite3')),
        conn_max_age=600,
        ssl_require=True if config('DATABASE_URL', default='').startswith('postgres') else False
    )
}

INSTALLED_APPS += ['debug_toolbar', 'django_extensions']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

HOSPITAL_NAME = "Gestión de Bienes Patrimoniales - Hospital Melchor Romero (Desarrollo)"

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'


