import os

from celery import Celery
from django.conf import settings

if settings.DEBUG:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "braniaclms.settings")

celery_app = Celery("braniaclms")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
