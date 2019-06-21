from django.shortcuts import render
from django.views.generic import ListView
from images.models import *
from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from images.serializers import VideoSerializer, AlbumSerializer
import json

# Create your views here.
class HomePageView(ListView):
    model = Video
    template_name = 'home.html'

class VideoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows videos to be viewed or edited.
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class AlbumViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows albums to be viewed or edited.
    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class FileUploadView(APIView):
    #parser_classes = (MultiPartParser, FormParser)


    def check_pin(user_pin, y):
        s = Album.objects.get(pin=y).status
        if s == 'o':
            return True
        else:
            return False

    def post(self, request, *args, **kwargs):
        #file_serializer = FileSerializer(data=request.data)
        #if file_serializer.is_valid():
            #file_serializer.save()
        #print(request.body)
        data = base64.decode(request.body)
        print(data)
        video_data = json.loads(data)
        #print(video_data)
        if self.check_pin(video_data["pin"]):
            video = Video.create(video_data["title"], video_data["file"], video_data['pin'])
            video.save()
            return Response(video_data, status=status.HTTP_201_CREATED)
        elif file_serializer.check_pin(file_serializer.data['pin']) == False:
            return Response({'pin': Album.objects.get(pin=video_data['pin']).name + ' album is closed.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(video_data, status=status.HTTP_400_BAD_REQUEST)
