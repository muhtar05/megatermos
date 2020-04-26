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

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'djabrail-92_megatermos',  # Or path to database file if using sqlite3.
#         'USER': '046014525_mega',
#         'PASSWORD': 'mega2020termos',
#         'HOST': '127.0.0.1',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
#         # Set to empty string for default.
#     }
# }