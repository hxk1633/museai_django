from django.contrib import admin
import os

# Register your models here.
from images.models import Video, Album, TFModel


def close_album(modeladmin, request, queryset):
    queryset.update(status='c')

def open_album(modeladmin, request, queryset):
    queryset.update(status='o')

close_album.short_description = "Close album to users"
open_album.short_description = "Make album available to users"

class AlbumAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'pin', 'status']
    ordering = ['name']
    actions = [close_album, open_album]

class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'album']
    ordering = ['title']

class TFModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'videos', 'album', 'accuracy']
    ordering = ['name']

admin.site.register(Album, AlbumAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(TFModel, TFModelAdmin)
