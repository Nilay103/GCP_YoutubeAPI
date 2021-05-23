# myapi/urls.py
from django.urls import include, path
from rest_framework import routers
from .views import YouTubeVideoViewSet, YouTubeVideoView

router = routers.DefaultRouter()
router.register('videos', YouTubeVideoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('', YouTubeVideoViewSet.as_view())
    path('lol', YouTubeVideoView.as_view())
]
