from django.shortcuts import render
from django.views.generic import ListView
from images.models import *
from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from images.serializers import VideoSerializer, AlbumSerializer
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import json
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import VideoForm
from django.http import JsonResponse
from django.shortcuts import render
from django_tables2 import RequestConfig
from .tables import AlbumTable
from django.contrib.auth.decorators import login_required


@login_required
def albums(request):
    table = AlbumTable(Album.objects.filter(organization=request.user).order_by('name'))
    RequestConfig(request).configure(table)
    return render(request, 'images/album_list_created_user.html', {'table': table})

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['table'] = AlbumTable(Album.objects.all(), _overriden_value="overriden value")

class AlbumsByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing albums to current user."""
    model = Album
    template_name ='images/album_list_created_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return Album.objects.filter(organization=self.request.user).order_by('name')

class AlbumCreate(LoginRequiredMixin, CreateView):
    model = Album
    fields = ['name','description']
    def form_valid(self, form):
        album = form.save(commit=False)
        album.organization =  self.request.user
        album.save()
        form.save_m2m()
        return redirect('/albums')

class AlbumEdit(LoginRequiredMixin, UpdateView):
    model = Album
    fields = ['name', 'description']
    template_name_suffix = '_edit_form'
    success_url = reverse_lazy('albums')

class AlbumDelete(LoginRequiredMixin, DeleteView):
    model = Album
    success_url = reverse_lazy('albums')

class HomePageView(ListView):
    model = Video
    template_name = 'home.html'

class BasicUploadView(LoginRequiredMixin, View):
    def get(self, request):
        video_list = Video.objects.all()
        return render(self.request, 'basic_upload/index.html', {'videos': video_list})

    def post(self, request):
        form = VideoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            video = form.save()
            data = {'is_valid': True, 'name': video.file.name, 'url': video.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

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
