"""
Base Django settings for datasite project.

Run using: python manage.py runserver --settings=dataentry.settings.base

"""
from __future__ import absolute_import  # Allow explicit relative imports

import os

from dataentry.email_info import EMAIL_USE_TLS, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT
from registration_defaults.settings import *  # For registration

import socket

# Will Added 5/10/2014, get from 'email_info.py'
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
#/Users/williamliu/GitHub/timetracker/datasite

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'lpd=mx^9_8c+dfw7p%rnxe!j0ive0xt87$5q1)54ww2nv*-*jb'

ALLOWED_HOSTS = ['10.1.1.7', 'test.com',]


# SECURITY WARNING: don't run with debug turned on in production!
if socket.gethostname() in (ALLOWED_HOSTS):
    DEBUG = False
else:
    DEBUG = True
#DEBUG_TOOLBAR_PATCH_SETTINGS = False # django-toolbar not to adjust your settings

#APIlink = 'http://127.0.0.1:8000/data/?format=json'

# Application definition

INSTALLED_APPS = (
    'registration_defaults',  # List before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'timesheets',
    'registration',
    'rest_framework', # For Django REST framework
    'debug_toolbar', # For Django Debug Toolbar 1.6
    #'tastypie',  # for Django Tastypie
)

ACCOUNT_ACTIVATION_DAYS = 7  # 1-week activation window
LOGIN_REDIRECT_URL = '/'  # After login, takes you back to this page instead of 'accounts/profile'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dataentry.urls'

WSGI_APPLICATION = 'dataentry.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

#DATABASES = {
#    'default': {
#        #MySQL - local
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'dataentry',
#        'USER': 'root',
#        'PASSWORD': '',
#        'HOST': '127.0.0.1',
#        'ATOMIC_REQUEST': True, # Ensures ACID
#
#        #MySQL - On Ubuntu Server
#        #'ENGINE': 'django.db.backends.mysql',
#        #'NAME': 'dataentry',
#        #'USER': 'root',
#        #'PASSWORD': 'test',
#        #'HOST': 'localhost',
#        #'PORT': '',
#
#        #Postgresql - On Ubuntu Server w/Postgresql - For Testing Only
#        #'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        #'NAME': 'dataentry',
#        #'USER': 'postgres',
#        #'PASSWORD': 'test',
#        #'HOST': 'localhost',
#        #'PORT': '',
#
#        #SQLLite
#        #'ENGINE': 'django.db.backends.sqlite3',
#        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#
#    }
#}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = '/media/'
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR), "datasite", "templates"),
    )
# '/templates' #'/Users/williamliu/GitHub/timetracker/datasite/templates/',

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR), "datasite", "static"),
    )

STATIC_ROOT = (
    os.path.join(os.path.dirname(BASE_DIR), "static")
    #"/Users/williamliu/GitHub/timetracker/datasite/static/",
    )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
    },
    'root': {'level': 'INFO'},
}

# Django REST Framework API
REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the 'serializer_class' attribute is not set on a view
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard 'django.contrib.auth' permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]

}
