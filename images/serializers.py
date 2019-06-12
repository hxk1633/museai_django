from .models import Video, Album, VideoFile, TFModel
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

class TFModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TFModel
        fields = ('name', 'album', 'objects')

    def get_objects(self, instance):
        return Video.objects.filter(album=self.album).count()
