from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'ery@#b7zsbl^vsz!d(qu86q^p(g__sk=^jkq(x2(zg0r^rna8_'
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# ==========================
# APLICACIONES INSTALADAS
# ==========================
INSTALLED_APPS = [
    # Django apps por defecto
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Tu app principal
    'core',  
]

# ==========================
# MIDDLEWARE
# ==========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# settings.py

AUTH_PASSWORD_VALIDATORS = [
    # ... los que ya estén ...
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    # AGREGÁ ESTA LÍNEA (ajustá "nombre_de_tu_app" al nombre real):
    {
        'NAME': 'core.validators.ComplexPasswordValidator',
    },
]

# ==========================
# URLS / WSGI
# ==========================
ROOT_URLCONF = 'sistema_bienes.urls'
WSGI_APPLICATION = 'sistema_bienes.wsgi.application'

# ==========================
# TEMPLATES
# ==========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ==========================
# BASE DE DATOS (SQLite local)
# ==========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_development.sqlite3',
    }
}

# ==========================
# ARCHIVOS ESTÁTICOS / MEDIA
# ==========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==========================
# AUTENTICACIÓN / LOGIN
# ==========================
AUTH_USER_MODEL = 'core.Usuario'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/inicio/'
LOGOUT_REDIRECT_URL = '/login/'

# ==========================
# REGIONAL.
# ==========================
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# ==========================
# EMAIL CONFIGURATION
# ==========================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'desposfrancisco@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password-here'  # Reemplaza con la App Password de Google
DEFAULT_FROM_EMAIL = 'desposfrancisco@gmail.com'

