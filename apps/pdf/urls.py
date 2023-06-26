from apps.pdf.views import *
from django.urls import path

urlpatterns = [
    path('merge', Merge.as_view(), name='merge'),
]
