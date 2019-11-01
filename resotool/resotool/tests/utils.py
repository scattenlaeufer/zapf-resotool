from celery.bin import base as celery_base
from celery.bin import celery as celery_bin
from celery import platforms as celery_platforms

from resotool import celery_app


celery_status = celery_bin.CeleryCommand.commands["status"]()
celery_status.app = celery_status.get_app()


def celery_is_up():
    """
    A utility function to check whether Celery is running or not.

    :returns bool: True if Celery is runing, False if not

    """
    try:
        celery_status.run()
        return True
    except celery_base.Error as e:
        if e.status == celery_platforms.EX_UNAVAILABLE:
            return False
        raise e
