"""
Create a Celery app to be used by Django.
"""

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resotool.settings")
app = Celery("resotool")  # pylint: disable=invalid-name

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    """
    A debug function to print the current request of the Celery app.
    """
    print("Request: {0!r}".format(self.request))
