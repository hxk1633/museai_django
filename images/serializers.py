from images.models import Video, Album, TFModel
from rest_framework import serializers
import base64


class VideoSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=50)
    pin = serializers.CharField(max_length=6)
    file = serializers.FileField(max_length=None, use_url=True)
    """
    def validate_title(self, value):
        if Album.objects.filter(name=value).exists():
            print("already exists")
            raise serializers.ValidationError('already exists')
        return value

    def validate_pin(self, value):
        try:
            print(value)
            Album.objects.get(pin=value).exits()
            print("Good")
        except:
            print("Invalid pin. Album doesn't exist.")
            raise serializers.ValidationError("Invalid pin. Album doesn't exist.")

        if Album.objects.get(pin=value).staus == 'c':
            raise serializers.ValidationError(Album.objects.get(pin=value).getAlbumName() + " is closed.")
        return value
    """

    def validate(self, data):
        if Album.objects.filter(name=data['title']).exists():
            print("already exists")
            raise serializers.ValidationError({'title':'already exists'})
        try:
            Album.objects.get(pin=data['pin'])
            print("Good pin")
        except:
            print("Invalid pin. Album doesn't exist.")
            raise serializers.ValidationError({'pin': 'Invalid pin. Album doesnt exist.'})

        if Album.objects.get(pin=data['pin']).status == 'c':
            print("album closed")
            raise serializers.ValidationError({"pin": Album.objects.get(pin=data['pin']).name + " is closed."})
        return data



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
