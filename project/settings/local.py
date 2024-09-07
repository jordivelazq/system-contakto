from .base import *

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % 'Contakto.Me'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.1and1.mx"
EMAIL_PORT = 587
EMAIL_HOST_USER = "estudios@contakto.mx"
EMAIL_HOST_PASSWORD = "Estudios-ckt1"
EMAIL_USE_TLS = False

HOST_SERVER = "http://127.0.0.1:8000"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db_contakto',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost'
    }
}

SHOW_DJANGO_TOOLBAR = True

INSTALLED_APPS = INSTALLED_APPS + ('rest_framework', 'drf_spectacular')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
       
    ),
    
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'oauth2_provider.contrib.rest_framework.TokenHasReadWriteScope',
    # ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_datatables.renderers.DatatablesRenderer',
    ),

    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_datatables.filters.DatatablesFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_datatables.pagination.DatatablesPageNumberPagination',
    'PAGE_SIZE': 50,
    
}