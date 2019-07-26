"""museai_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from images import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', include('images.urls')),
    path('', include('images.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('myalbums/', views.AlbumsByUserListView.as_view(), name='my-albums'),
    path('myalbums/create/', views.AlbumCreateView.as_view(), name='album_create'),
    path('myalbums/update/<int:pk>', views.AlbumUpdateView.as_view(), name='update_album'),
    path('myalbums/delete/<int:pk>', views.AlbumDeleteView.as_view(), name='delete_album'),
    path('basic-upload/<int:pk>', views.BasicUploadView.as_view(), name='basic_upload'),
    path('ajax/load-videos/', views.load_videos, name='ajax_load_videos')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
