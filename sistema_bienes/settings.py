from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'poné-tu-secret-key-aca'
DEBUG = True

ALLOWED_HOSTS = []

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
    'core',   # ← IMPORTANTE
]

# ==========================
# CONFIGURACIÓN DE TEMPLATES
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
# ARCHIVOS ESTÁTICOS
# ==========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",   # ← carpeta donde guardaste css, js, fonts, img
]

# ==========================
# BASE DE DATOS
# ==========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Indica que usarás tu modelo personalizado
AUTH_USER_MODEL = 'core.Usuario'  # Reemplaza 'tu_app' con el nombre de tu app

# URLs de redirección
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/inicio/'  # Cambiar a inicio para que maneje el rol correctamente
LOGOUT_REDIRECT_URL = '/login/'