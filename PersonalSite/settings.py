"""
Django settings for PersonalSite project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Nice try :)
try:
    from PersonalSite.secret_settings import *

except ImportError:
    SECRET_KEY = os.environ.get('SECRET_KEY', None)
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
    DYNAMO_ACCESS_KEY = os.environ.get('DYNAMO_ACCESS_KEY', None)
    DYNAMO_SECRET_ACCESS_KEY = os.environ.get('DYNAMO_SECRET_ACCESS_KEY', None)
    AUTH_TOKEN = os.environ.get('AUTH_TOKEN', None)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    'localhost',
    '82jfdcutig.execute-api.us-east-1.amazonaws.com',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',  # uncommented so rest_framework works
    'django.contrib.contenttypes',  # uncommented so rest_framework works
    'django.contrib.staticfiles',

    # main app
    'index',

    # blog
    'blog',

    # API
    'api',

    # S3 file storage
    'storages',

    # DynamoDB
    'django_dynamodb',

    # django rest framework
    'rest_framework',

    # work experience
    'workexperience',

    # fun links
    'funlinks',

    # corsheaders
    'corsheaders',
]


MIDDLEWARE = [
    # gzip
    # API gateway currently does not support HTTP compression. It is on the roadmap
    # for now this remains commented out. All static files are gzipped anyway.
    # 'django.middleware.gzip.GZipMiddleware',

    # cors middleware
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PersonalSite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                # 'django.contrib.auth.context_processors.auth',
                # 'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'PersonalSite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

AWS_STORAGE_BUCKET_NAME = 'lucas-simpson-personal-site-static'
AWS_ACCESS_KEY_ID = 'AKIAIHOL64GDXSEZWXJQ'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_IS_GZIPPED = True  # enable gzip compression

# use local for dev
if DEBUG:
    STATIC_URL = '/static/'
else:
    STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

# Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
# you run `collectstatic`).
if not DEBUG:
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# DynamoDB
DYNAMO_TABLE_PREFIX = 'PersonalSite'

# Django Rest Framework
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.auth.IsLucasAuthentication'
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

# cors. No way to whitelist chrome extension, so here we are
CORS_ORIGIN_ALLOW_ALL = True

