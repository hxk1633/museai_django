from .models import Video, Album, VideoFile
from rest_framework import serializers


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = ('url', 'title', 'album', 'file')


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Album
        fields = ('url', 'name', 'description', 'pin', 'status')


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = ('title', 'file', 'pin')
