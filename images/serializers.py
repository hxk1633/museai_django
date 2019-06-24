from images.models import Video, Album, TFModel
from rest_framework import serializers
import base64


class VideoSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=50)
    pin = serializers.CharField(max_length=6)
    file = serializers.FileField(max_length=None, use_url=True)

    class Meta:
        model = Video
        fields = ('title', 'pin', 'file')


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('url', 'name', 'description', 'pin', 'status')
"""
class FileSerializer(serializers.ModelSerializer):
    def check_pin(pin, y):
        s = Album.objects.get(pin=y).status
        if s == 'o':
            return True
        else:
            return False

    class Meta:
        model = VideoFile
        fields = ('title', 'file', 'pin')
"""
class TFModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TFModel
        fields = ('name', 'album', 'videos')
