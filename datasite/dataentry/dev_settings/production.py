"""
Production Django settings for datasite project.

Run using: python manage.py runserver --settings=dataentry.settings.production

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from __future__ import absolute_import  # Allow explicit relative imports

from .base import *

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES = {
    'default': {

        #MySQL - On Ubuntu Server
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dataentry',
        'USER': 'root',
        'PASSWORD': 'test',
        'HOST': 'localhost',
        'PORT': '',
        'ATOMIC_REQUEST': True, # Ensures ACID
    }
}

