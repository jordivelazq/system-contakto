from .base import *
import os
# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.environ['CONTAKTO_DB_NAME'],
        'USER': os.environ['CONTAKTO_DB_USER'],                      # Not used with sqlite3.
        'PASSWORD': os.environ['CONTAKTO_DB_PASSWORD'],                  # Not used with sqlite3.
        'HOST': os.environ['MYSQL_CONTAKTO_PORT_3306_TCP_ADDR']                      # Set to empty string for localhost. Not used with sqlite3.
    }
}
