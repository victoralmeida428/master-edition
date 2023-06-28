from apps.geoloc.views import *
from django.urls import path

urlpatterns = [
    path('geoloc', GeoLoc.as_view(), name='geoloc'),
]
