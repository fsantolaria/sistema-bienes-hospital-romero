from .base import *
from decouple import config, Csv

DEBUG = False

# En Vercel, ALLOWED_HOSTS debe incluir el dominio .vercel.app
# Configurar en las variables de entorno de Vercel: ALLOWED_HOSTS=tu-app.vercel.app,www.tu-dominio.com
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1',
    cast=Csv()
)

# Base de datos — en producción usar PostgreSQL (Neon)
# Si DATABASE_URL está definida, usar PostgreSQL; sino SQLite como fallback
_db_url = config('DATABASE_URL', default='')
if _db_url:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(_db_url, conn_max_age=600, ssl_require=True)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

HOSPITAL_NAME = config(
    'HOSPITAL_NAME',
    default='Gestión de Bienes Patrimoniales - Hospital Melchor Romero'
)

# Seguridad para producción
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'