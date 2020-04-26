# Megatermos

В файле .gitignore находятся manage.py и megatermos/settings/local_settings.py 
Эти файлы нужно создать вручную для локальной разработки

Содержимое **manage.py**
```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'megatermos.settings.local_settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()`
```

Содержимое файла **megatermos/settings/local_settings.py**
```python
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

# INSTALLED_APPS += [
# ]


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
В этих файлах будут специфичные настройки для локальной разработки. 


Установка необходимых зависимостей

`pip install -r requirements.txt`

Выполнение миграций
 
`python manage.py migrate`

Команда для загрузки товаров из Excel файла в БД(Пока используется Sqlite )

`python manage.py add_products`





