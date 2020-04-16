from __future__ import absolute_import

import os
import django

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
# import django settings, in order to run django "standalone" (eg. models)
django.setup()

app = Celery('judge-service')

app.config_from_object('django.conf:settings')

# checking for all tasks for each django apps
# https://docs.celeryproject.org/en/stable/reference/celery.html#celery.Celery.autodiscover_tasks
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)