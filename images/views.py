from django.shortcuts import render
from django.views.generic import ListView
from .models import Album


# Create your views here.
class HomePageView(ListView):
    model = Album
    template_name = 'home.html'
    
