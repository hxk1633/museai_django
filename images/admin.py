from django.contrib import admin
import os
import time
from images.models import Video, Album, TFModel
from images.tasks import new_model
# Register your models here.

def close_album(modeladmin, request, queryset):
    queryset.update(status='c')

def open_album(modeladmin, request, queryset):
    queryset.update(status='o')

def create_model(modeladmin, request, queryset):
    for album in queryset:
        new_model.apply_async(args=[album.id], countdown=5)

close_album.short_description = "Close album to users"
open_album.short_description = "Make album available to users"
create_model.short_description = "Train model"

class AlbumAdmin(admin.ModelAdmin):
    list_display = ['organization', 'name', 'description', 'pin', 'model_status', 'status']
    ordering = ['name']
    actions = [close_album, open_album, create_model]

class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'album']
    ordering = ['title']

class TFModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'album_model']
    ordering = ['name']

admin.site.register(Album, AlbumAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(TFModel, TFModelAdmin)
