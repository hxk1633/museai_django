from django.urls import include, path
from rest_framework import routers
from django.conf.urls import url
from .views import *
from . import views

from .views import HomePageView

router = routers.DefaultRouter()
router.register(r'videos', VideoViewSet)
router.register(r'albums', AlbumViewSet)

api_urlpatterns = ([
    url('', include(router.urls)),
], 'api')

urlpatterns = [
    url(r'^api/', include(api_urlpatterns)),
    url(r'^basic-upload/$', views.BasicUploadView.as_view(), name='basic_upload'),
    url(r'^albums/', albums, name='albums'),
    url(r'^actions_albums/$', Albums_Actions, name='actions-albums')
]
