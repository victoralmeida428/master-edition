from apps.user.views import *
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('cadastro', Cadastro.as_view(), name='cadastro'),
    path('logout', logout, name='logout'),
]
