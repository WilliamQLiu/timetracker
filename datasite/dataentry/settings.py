"""
Base Django settings for datasite project.

Run using: python manage.py runserver --settings=dataentry.settings.base

"""
from __future__ import absolute_import  # Allow explicit relative imports

import os
from registration_defaults.settings import *  # For registration
import socket
from dataentry.email_info import EMAIL_USE_TLS, EMAIL_HOST, EMAIL_HOST_USER, \
    EMAIL_HOST_PASSWORD, EMAIL_PORT

# Will Added 5/10/2014, get from 'email_info.py'
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'lpd=mx^9_8c+dfw7p%rnxe!j0ive0xt87$5q1)54ww2nv*-*jb'

ALLOWED_HOSTS = ['10.1.1.7', 'test.com',]  # 10.1.1.7 is arbitrary IP

DEBUG = True
TEMPLATE_DEBUG = True
#DEBUG_TOOLBAR_PATCH_SETTINGS = False # django-toolbar not to adjust settings

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
    'temp',
    'registration',
    'rest_framework', # For Django REST framework
    'debug_toolbar', # Activate Django Debug Toolbar 1.6
    #'djcelery', # For scheduled celery tasks (celery-beat)
)

AUTH_PROFILE_MODULE = 'timesheets.UserProfile'  # this app extends our default User

# Django-Registration
ACCOUNT_ACTIVATION_DAYS = 7  # 1-week activation window
LOGIN_REDIRECT_URL = '/'  # After login, redirects instead 'accounts/profile'

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # django-debug-toolbar
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dataentry.urls'

WSGI_APPLICATION = 'dataentry.wsgi.application'


DATABASES = {
    'default': {

        #MySQL - local
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dataentry',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',

        #MySQL - On Ubuntu Server
        #'ENGINE': 'django.db.backends.mysql',
        #'NAME': 'dataentry',
        #'USER': 'root',
        #'PASSWORD': 'test',
        #'HOST': 'localhost',
        #'PORT': '',
        #'ATOMIC_REQUEST': True, # Ensures ACID
    }
}

# Celery configurations
BROKER_URL = 'redis://127.0.0.1:6379/0'
BROKER_TRANSPORT = 'redis'
# Access our database and pull out tasks at scheduled times and send to queue
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
#CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = (
    os.path.join(os.path.dirname(BASE_DIR), "media")
    )
MEDIA_URL = '/media/'

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
STATIC_URL = '/static/'


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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
        #'LOCATION': 'unique-snowflake'
    }
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
