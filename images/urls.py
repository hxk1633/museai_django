from django.urls import include, path
from rest_framework import routers
from django.conf.urls import url
from .views import *

from .views import HomePageView

router = routers.DefaultRouter()
router.register(r'videos', VideoViewSet)
router.register(r'albums', AlbumViewSet)

api_urlpatterns = ([
    url('', include(router.urls)),
], 'api')

urlpatterns = [
    url(r'^api/', include(api_urlpatterns)),
]
