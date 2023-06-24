from apps.word.views import *
from django.urls import path

urlpatterns = [
    path('word', word_index, name='word'),
]
