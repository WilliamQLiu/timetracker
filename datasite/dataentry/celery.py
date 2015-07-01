""" Settings to setup celery """

from __future__ import absolute_import

import os
import django

from celery import Celery
from django.conf import settings

# Reference our default settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dataentry.settings')

app = Celery('dataentry')

app.config_from_object('django.conf:settings') # Use our project settings
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) # Look for python files
