from django.shortcuts import render
from django.views.generic import View
from apps.pdf.forms import PdfInput
from apps.geoloc.dash import Mapa
import pandas as pd
from time import time
# Create your views here.

class GeoLoc(View):
    template_name='geoloc/index.html'
    class_form = PdfInput

    def get(self, request):
        form = self.class_form()
        df = pd.DataFrame({'CEP':['23012-120', '23085-110','23090-820']})
        inicio=time()
        mapa = Mapa(df).criar_mapa()
        fim = time()
        print(fim-inicio)
        context ={
            'form':form,
            'button': 'Pegar Coordenadas',
            'dash': mapa
        }
        return render(request, self.template_name, context)
    

        
