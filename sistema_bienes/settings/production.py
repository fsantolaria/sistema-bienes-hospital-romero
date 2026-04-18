from .base import *
import dj_database_url

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///' + str(BASE_DIR / 'db_hospital.sqlite3')),
        conn_max_age=600,
        ssl_require=True if config('DATABASE_URL', default='').startswith('postgres') else False
    )
}

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

HOSPITAL_NAME = "Gestión de Bienes Patrimoniales - Hospital Melchor Romero"