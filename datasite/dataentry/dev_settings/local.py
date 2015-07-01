"""
Dev Django settings for datasite project.

Run using: python manage.py runserver --settings=dataentry.settings.local

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from __future__ import absolute_import  # Allow explicit relative imports

from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        #MySQL - local
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dataentry',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'ATOMIC_REQUEST': True, # Ensures ACID
    }
}

# Celery
BROKER_URL = 'redis://127.0.0.1:6379/0'
BROKER_TRANSPORT = 'redis'
# Access our database and pull out tasks at scheduled times and send to queue
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
