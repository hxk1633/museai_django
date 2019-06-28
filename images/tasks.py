from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils.crypto import get_random_string
from images.models import Album, TFModel
import time
from subprocess import Popen, PIPE

@shared_task
def new_pins():
    albums = Album.objects.all()
    for a in albums:
        a.pin = get_random_string(length=6).upper()
        a.save()

@shared_task
def new_model(album_id):
    album = Album.objects.get(id=album_id)
    gpu_machine = ["", "", ""]
    system_clean = ["docker", "system", "prune"]
    build_cmd = ["nvidia-docker", "build", ".", "-t", "model-builder"]
    run_cmd = ["nvidia-docker", "run", "-v", "/home/cat/Desktop/museai_django/media/albums/" + album.name + "/data:/data", "-it", "model-builder"]
    Album.objects.filter(name=album.name).update(model_status='t')
    build = Popen(build_cmd, stdout=PIPE)
    run = Popen(run_cmd, stdout=PIPE)
    while build.poll() is None:
        time.sleep(0.5)
    print("build done")
    while run.poll() is None:
        time.sleep(0.5)
    print("model created")
    Album.objects.filter(name=album.name).update(model_status='c')
    tfmodel = TFModel.objects.create(name=album.name, album=album, accuracy=100)
