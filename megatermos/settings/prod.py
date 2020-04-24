from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(os.path.expanduser('~'), 'domains/megatermos24.ru/assets/')
MEDIA_ROOT = os.path.join(os.path.expanduser('~'), 'domains/megatermos24.ru/media/')