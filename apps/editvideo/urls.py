from apps.editvideo.views import *
from django.urls import path

urlpatterns = [
    path('video', video_index, name='video'),
]
