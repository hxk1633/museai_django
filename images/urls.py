from django.urls import include, path
from rest_framework import routers
from django.conf.urls import url
from .views import VideoViewSet, AlbumViewSet, FileUploadView

from .views import HomePageView

router = routers.DefaultRouter()
router.register(r'videos', VideoViewSet)
router.register(r'albums', AlbumViewSet)



urlpatterns = [
    #path('', HomePageView.as_view(), name='home'),
    path('', include(router.urls)),
    url(r'^upload_video/$', FileUploadView.as_view(), name="video-upload"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
