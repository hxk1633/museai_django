from django.shortcuts import render
from django.views.generic import ListView
from .models import Video


# Create your views here.
class HomePageView(ListView):
    model = Video
    template_name = 'home.html'
