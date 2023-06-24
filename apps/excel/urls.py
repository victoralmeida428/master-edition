from apps.excel.views import *
from django.urls import path

urlpatterns = [
    path('excel', Excel.as_view(), name='excel'),
]
