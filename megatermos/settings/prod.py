from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(os.path.expanduser('~'), 'domains/megatermos24.ru/assets/')
MEDIA_ROOT = os.path.join(os.path.expanduser('~'), 'domains/megatermos24.ru/media/')

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "djabrail-92_megatermos",
        "USER": "djabrail-92_megatermos",                             # Not used with sqlite3.
        "PASSWORD": "mega2020termos",                         # Not used with sqlite3.
        "HOST": "/var/run/postgresql",                             # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "",                             # Set to empty string for default. Not used with sqlite3.
    }
}