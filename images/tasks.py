from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils.crypto import get_random_string
from images.models import Album

@shared_task
def new_pin(old_pin):
    a = Album.objects.get(pin=old_pin)
    a.pin = get_random_string(length=6).upper()
    a.save()
