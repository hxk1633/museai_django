from django.shortcuts import render
from django.views.generic import ListView
from images.models import *
from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from images.serializers import VideoSerializer, AlbumSerializer
from django.views.generic.edit import CreateView, DeleteView
import json
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class AlbumsByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing albums to current user."""
    model = Album
    template_name ='images/album_list_created_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Album.objects.filter(organization=self.request.user).order_by('name')

class AlbumCreate(CreateView):
    model = Album
    fields = '__all__'

class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('myalbums')

class HomePageView(ListView):
    model = Video
    template_name = 'home.html'

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    class Meta:
        ordering = ['-id']

    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.title, serializer.file, serializer.pin)
            serializer.save()
            return Response("Your video has been uploaded!", status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors)

class AlbumViewSet(viewsets.ModelViewSet):

    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
