from django.shortcuts import render
from django.views.generic import View
from apps.geoloc.forms import ExcelInput
from apps.geoloc.dash import Mapa
import pandas as pd
from time import time
# Create your views here.

class GeoLoc(View):
    template_name='geoloc/index.html'
    class_form = ExcelInput

    def get(self, request):
        form = self.class_form()
        context ={
            'form':form,
            'button': 'Pegar Coordenadas',
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.class_form(request.POST, request.FILES)
        df = pd.DataFrame({'CEP':['0000000']})
        col = 'CEP'
        if form.is_valid():
            file = request.FILES.getlist('files')[0]
            col = form.cleaned_data['busca']
            df = pd.read_excel(file)
        
        Mapa(df, col).criar_mapa()
        context ={
            'form':form,
            'button': 'Pegar Coordenadas',
        }
        return render(request, self.template_name, context)
    

        
