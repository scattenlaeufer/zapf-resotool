"""
Setting to make Celery app usable in Django apps
"""

from .celery import app as celery_app

__all__ = ("celery_app",)
