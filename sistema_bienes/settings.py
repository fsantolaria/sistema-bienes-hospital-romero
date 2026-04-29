from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ⚠️ Cambiá esto por una clave segura en producción
SECRET_KEY = 'poné-tu-secret-key-aca'
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
    'core',  # Asegurate que exista core/apps.py y esté en INSTALLED_APPS
]

# ==========================
# MIDDLEWARE
# ==========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==========================
# URLS / WSGI
# ==========================
ROOT_URLCONF = 'sistema_bienes.urls'   # ← ajustá al nombre real de tu proyecto (carpeta con urls.py)
WSGI_APPLICATION = 'sistema_bienes.wsgi.application'  # ← idem

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
# BASE DE DATOS (SQLite)
# ==========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # Podés cambiar a BASE_DIR / 'db/produccion.sqlite3' si preferís esa ruta
        'NAME': BASE_DIR / 'db_development.sqlite3',
    }
}

# ==========================
# ARCHIVOS ESTÁTICOS / MEDIA
# ==========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",   # donde tenés css/js/fotos fuente
]
STATIC_ROOT = BASE_DIR / "staticfiles"  # destino de collectstatic

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==========================
# AUTENTICACIÓN / LOGIN
# ==========================
AUTH_USER_MODEL = 'core.Usuario'  # asegurate que el modelo exista
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/inicio/'
LOGOUT_REDIRECT_URL = '/login/'   # ← sin punto al final

# ==========================
# REGIONAL.
# ==========================
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True
