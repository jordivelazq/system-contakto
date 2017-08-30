from .base import *
import os
# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'system',
        'USER': os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],                      # Not used with sqlite3.
        'PASSWORD': os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],                  # Not used with sqlite3.
        'HOST': os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],                      # Set to empty string for default. Not used with sqlite3.
    }
}
