from apps.pdf.views import *
from django.urls import path

urlpatterns = [
    path('merge', Merge.as_view(), name='merge'),
    path('merge_sucess', merge_sucess, name='merge_sucess'),
]
