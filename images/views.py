from django.shortcuts import render
from django.views.generic import ListView
from images.models import *
from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from images.serializers import VideoSerializer, AlbumSerializer, FileSerializer



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
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        """
        serializer_context = {
            'request': request,
        }
        """
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            video = Video.create(file_serializer.data['title'], file_serializer.data['file'], file_serializer.data['pin'])
            video.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
