from apps.word.views import *
from django.urls import path

urlpatterns = [
    path('word', Word.as_view(), name='word'),
]
