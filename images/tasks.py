from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils.crypto import get_random_string
from images.models import Album, TFModel
import time
import os
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
    #gpu_machine = ["", "", ""]
    system_clean = ["docker", "system", "prune", "-a"]
    build_cmd = ["docker", "build", "-t", "model-builder", "."]
    run_cmd = ["docker", "run", "-v", "/home/django/museai_django/media/albums/" + album.name + "/data:/data", "-it", "model-builder"]
    Album.objects.get(id=album_id).update(model_status='t')
    build = Popen(build_cmd, stdout=PIPE)
    run = Popen(run_cmd, stdout=PIPE)
    print("model created")
    print(build.communicate())
    print(run.communicate())
    Album.objects.get(id=album_id).update(model_status='c')
    tfmodel = TFModel.objects.create(name=album.name, album_model=album)

@shared_task
def visualize_data():
    os.system("killall -v tensorboard")
    models = Album.objects.filter(model_status='c')
    cmd = "tensorboard --logdir="
    count = 0
    for model in models:
        if count > 0:
            cmd += ","
        name = model.name.replace(" ", "_")
        cmd += name.lower() + ":/home/harrison/Desktop/museai_django/media/albums/" + name + "/data/summaries"
        count += 1
    print(cmd)
    run_tensorboard = Popen(cmd.split(" "), stdout=PIPE)
