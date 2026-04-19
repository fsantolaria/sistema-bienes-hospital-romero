from .base import *

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Base de datos SQLite (solo uso local)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

HOSPITAL_NAME = "Gestión de Bienes Patrimoniales - Hospital Melchor Romero"