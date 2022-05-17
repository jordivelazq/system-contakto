from .base import *
import os
import environ

env = environ.Env()

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': env.db('CONTAKTO_DB_NAME'),
        'USER': env.db('CONTAKTO_DB_USER'),                      # Not used with sqlite3.
        'PASSWORD': env.db('CONTAKTO_DB_PASSWORD'),                  # Not used with sqlite3.
        'HOST': env.db('MYSQL_CONTAKTO_PORT_3306_TCP_ADDR')                      # Set to empty string for localhost. Not used with sqlite3.
    }
}

SHOW_DJANGO_TOOLBAR = False
