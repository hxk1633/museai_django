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

class TFModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TFModel
        fields = ('name', 'album', 'videos')
