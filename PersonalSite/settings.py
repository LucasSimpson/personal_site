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
    import secret_settings
    SECRET_KEY = secret_settings.SECRET_KEY
    AWS_SECRET_ACCESS_KEY = secret_settings.AWS_SECRET_ACCESS_KEY
    DYNAMO_ACCESS_KEY = secret_settings.DYNAMO_ACCESS_KEY
    DYNAMO_SECRET_ACCESS_KEY = secret_settings.DYNAMO_SECRET_ACCESS_KEY

except ImportError:
    SECRET_KEY = os.environ.get('SECRET_KEY', None)
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
    DYNAMO_ACCESS_KEY = os.environ.get('DYNAMO_ACCESS_KEY', None)
    DYNAMO_SECRET_ACCESS_KEY = os.environ.get('DYNAMO_SECRET_ACCESS_KEY', None)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    'localhost' if DEBUG else '82jfdcutig.execute-api.us-east-1.amazonaws.com',
]


# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',

    # main app
    'index',

    # S3 file storage
    'storages',

    # DynamoDB
    'django_dynamodb',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
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
