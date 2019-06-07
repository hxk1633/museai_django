from django.contrib import admin
from ffmpy import FFmpeg
import os

# Register your models here.
from .models import Video, Album


def createAlbum(modeladmin, request, queryset):
    for video in queryset:
        queryset.filter(title=video.title).update(status='p')
        os.mkdir('media/albums/' + video.getFileName())
        convert = FFmpeg(inputs={video.getFilePath(): None}, outputs={"media/videos/" + video.getFileName() + ".mp4": None})
        ff = FFmpeg(inputs={"media/videos/" + video.getFileName() + ".mp4": None}, outputs={"media/albums/" + video.getFileName() + "/" + video.getFileName() + "%d.png": ['-vf', 'fps=2']})
        convert.run()
        ff.run()
        queryset.filter(title=video.title).update(status='c')

createAlbum.short_description = "Create album"

class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    ordering = ['title']
    actions = [createAlbum]

admin.site.register(Video, VideoAdmin)
admin.site.register(Album)
