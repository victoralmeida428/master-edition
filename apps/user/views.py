from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.views.generic import FormView
from apps.user.forms import CadastroForm


def index(request):
    return render(request, 'index.html')

def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout efetuado com sucesso')
    return redirect('index')

class Cadastro(FormView):
    template_name = "user/cadastro.html"
    form_class = CadastroForm
    success_url = "/"

