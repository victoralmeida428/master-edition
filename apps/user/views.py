from typing import Any, Dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView
from django.contrib.auth.models import User
from apps.user.forms import CadastroForm, LoginForm


def index(request):
    return render(request, 'home/index.html')

class Login(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form) -> HttpResponse:
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = User.objects.get(username=username)
        nome = f'{user.first_name} {user.last_name}'.title()
        user = auth.authenticate(username=username, password=password)
        auth.login(self.request, user)
        messages.success(self.request, f'Bem-Vindo, {nome}')
        return super().form_valid(form)



def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout efetuado com sucesso')
    return redirect('index')

class Cadastro(FormView):
    template_name = "cadastro.html"
    form_class = CadastroForm
    success_url = "/"

    def form_valid(self, form) -> HttpResponse:
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        email = form.cleaned_data.get('email')
        new_user = User(username=username,
                        password=password,
                        email=email,
                        first_name= first_name,
                        last_name=last_name)
        new_user.save()
        user = auth.authenticate(username=username, password=password)
        auth.login(self.request, user)
        messages.success(self.request, f'Seja bem vindo, {first_name} {last_name}')
        return super().form_valid(form)

