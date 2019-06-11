from django.contrib import admin
import os

# Register your models here.
from .models import Video, Album


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

admin.site.register(Album, AlbumAdmin)
admin.site.register(Video, VideoAdmin)
