# sistema_bienes/settings_local.py

from .settings import *   # Heredo TODO del settings base
from pathlib import Path
import os

# Si por alguna razón el base no definió BASE_DIR, lo defino:
if "BASE_DIR" not in globals():
    BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

# --- INSTALLED_APPS obligatorio en local (forzado/extendido) ---
base_apps = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
try:
    INSTALLED_APPS  # existe?
except NameError:
    INSTALLED_APPS = []
# agrego los que falten
for a in base_apps:
    if a not in INSTALLED_APPS:
        INSTALLED_APPS.append(a)
# tu app principal (asegurala)
if 'core' not in INSTALLED_APPS:
    INSTALLED_APPS.append('core')

# --- MIDDLEWARE mínimo (por si el base no lo tenía) ---
default_middleware = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
try:
    MIDDLEWARE
except NameError:
    MIDDLEWARE = default_middleware
else:
    if not MIDDLEWARE:
        MIDDLEWARE = default_middleware

# --- TEMPLATES fallback (requerido por admin) ---
try:
    TEMPLATES
except NameError:
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
else:
    # si existe pero viene vacío, lo defino igual
    if not TEMPLATES:
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

# --- URLs/WSGI (ajustá si tu paquete se llama distinto) ---
ROOT_URLCONF = os.environ.get('ROOT_URLCONF', 'sistema_bienes.urls')
WSGI_APPLICATION = os.environ.get('WSGI_APPLICATION', 'sistema_bienes.wsgi.application')

# --- DB local forzada (SQLite) ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db_development.sqlite3",
    }
}

# --- Hosts y estáticos/medios ---
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = list(set(
    list(globals().get("STATICFILES_DIRS", [])) + [BASE_DIR / "static"]
))

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

