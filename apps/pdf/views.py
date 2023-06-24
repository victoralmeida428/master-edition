from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView
from apps.pdf.forms import PdfInput
import PyPDF2
from django.views import View
from django.shortcuts import render
from .forms import PdfInput
import io

class Merge(View):
    template_name = "pdf/merge.html"
    form_class = PdfInput
    success_url = "merge_sucess"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('files')
            merge = PyPDF2.PdfMerger()
            [merge.append(file) for file in files]
            
             # Criando um buffer para armazenar o PDF gerado
            output_buffer = io.BytesIO()
            merge.write(output_buffer)
            merge.close()
            
            # Configurando a resposta HTTP com o PDF gerado
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="merged_file.pdf"'
            response.write(output_buffer.getvalue())
            
            return response
        else:
            return render(request, self.template_name, {'form': form})

    
def merge_sucess(request):
    return render(request, 'pdf/merge_sucess.html')

