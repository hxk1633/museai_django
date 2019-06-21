from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def new_pin(album_object):
    album_object.pin = get_random_string(length=6).uppper()
    album_object.save()
