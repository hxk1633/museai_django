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
from .forms import VideoForm, AlbumForm
from django.http import JsonResponse
from django.shortcuts import render
from django_tables2 import RequestConfig
from .tables import AlbumTable
from django.contrib.auth.decorators import login_required
from bootstrap_modal_forms.generic import (BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)
from bootstrap_modal_forms.mixins import PassRequestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from images.tasks import new_model
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.contrib import messages


@login_required
def albums(request):
    table = AlbumTable(Album.objects.filter(organization=request.user).order_by('name'))
    RequestConfig(request).configure(table)
    return render(request, 'images/album_list_created_user.html', {'table': table})

@csrf_exempt #Add this too.
def Albums_Actions(request, id=None):

    if request.method == 'POST':
        if 'delete' in request.POST:
            id_list = request.POST.getlist('selection')
            print(id_list)
            for album_id in id_list:
                Album.objects.get(pk=album_id).delete()
            return HttpResponseRedirect(reverse_lazy('albums'))
        elif 'train' in request.POST:
            id_list = request.POST.getlist('selection')
            print("train-button: " + str(id_list[0]))
            videos = Video.objects.filter(album_id=int(id_list[0]))
            if len(videos) >= 2:
                print("id list" + str(id_list))
                for album_id in id_list:
                    album = Album.objects.get(pk=album_id)
                    new_model.apply_async(args=[album.id], countdown=5)
                return HttpResponseRedirect(reverse_lazy('albums'))
            else:
                messages.error(request, "Action not permitted! You must upload at least two videos to an album to train.")
                return HttpResponseRedirect(reverse_lazy('albums'))


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

class AlbumCreateView(BSModalCreateView, PassRequestMixin):
    template_name = 'images/album_form.html'
    form_class = AlbumForm
    success_message = 'Success: Album was created.'
    success_url = reverse_lazy('albums')
    """
    def get_form_kwargs(self, **kwargs):
        kwargs = super(PassRequestMixin, self).get_form_kwargs()
        kwargs.update({"organization": self.request.user})
        return kwargs
        """

    """
    def get_initial(self):
        return { 'organization': self.request.user }
    """


class AlbumUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Album
    template_name = 'images/album_edit_form.html'
    form_class = AlbumForm
    success_message = 'Success: Album was updated.'
    success_url = reverse_lazy('albums')

class AlbumDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Album
    template_name = 'images/album_confirm_delete.html'
    success_message = 'Success: Album was deleted.'
    success_url = reverse_lazy('albums')

class HomePageView(ListView):
    model = Video
    template_name = 'home.html'

class BasicUploadView(LoginRequiredMixin, View):
    def get(self, request):
        video_list = Video.objects.all()
        return render(self.request, 'basic_upload/index.html', {'videos': video_list})

    def post(self, request, pk):
        form = VideoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            video = form.save(pk, self.request.FILES['file'].name)
            data = {'is_valid': True, 'name': video.file.name,  'url': video.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    class Meta:
        ordering = ['title']

    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.title, serializer.file, serializer.pin)
            serializer.save()
            return Response("Your video has been uploaded!", status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors)

class VideoDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Video
    template_name = "videos/video_confirm_delete.html"
    success_message = 'Success: Video was deleted.'
    success_url = reverse_lazy('albums')


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

def load_videos(request):
    album_id = request.GET.get('album')
    print(album_id)
    videos = Video.objects.filter(album_id=album_id).order_by('title')
    print(videos)
    return render(request, 'videos/load_videos.html', {'videos': videos})

def get_status(request):
    albums_id = json.loads(request.GET.get('albums'))
    print("id-list (get-status)" + str(albums_id))
    model_statuses = []
    for id in albums_id:
        print("id (get-status)" + str(id))
        status = Album.objects.get(pk=int(id)).model_status
        model_statuses.append(status)
    print(model_statuses)
    return HttpResponse(json.dumps(model_statuses), content_type='application/json')
