from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils.crypto import get_random_string
from images.models import Album, TFModel

@shared_task
def new_pins():
    albums = Album.objects.all()
    for a in albums:
        a.pin = get_random_string(length=6).upper()
        a.save()

@shared_task
def new_model(album):
    build_cmd = ['docker', 'build', '.', '-t', 'model-builder1']
    run_cmd = ['docker', 'run', '-v', "/home/cat/Desktop/museai_webapp/media/albums/" + album.name + "/data:/data", '-it', 'model-builder1']
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
