from django.contrib import admin
import os
import time
from images.models import Video, Album, TFModel
from images.tasks import new_pin
from subprocess import Popen, PIPE
# Register your models here.

def close_album(modeladmin, request, queryset):
    queryset.update(status='c')

def open_album(modeladmin, request, queryset):
    queryset.update(status='o')

def generate_pin(modeladmin, request, queryset):
    for album in queryset:
        new_pin.apply_async(args=[album.pin], countdown=10)

def create_model(modeladmin, request, queryset):
    for album in queryset:
        build_cmd = ['nvidia-docker', 'build', '.', '-t', 'model-builder1']
        run_cmd = [ 'nvidia-docker', 'run', '-v', "/home/cat/Desktop/museai_webapp/media/albums/" + album.name + "/data:/data", '-it', 'model-builder1']
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

close_album.short_description = "Close album to users"
open_album.short_description = "Make album available to users"
create_model.short_description = "Create model"
generate_pin.short_description = "Generate new pin"

class AlbumAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'pin', 'model_status', 'status']
    ordering = ['name']
    actions = [close_album, open_album, create_model, generate_pin]

class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'album']
    ordering = ['title']

class TFModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'album', 'accuracy']
    ordering = ['name']

admin.site.register(Album, AlbumAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(TFModel, TFModelAdmin)
