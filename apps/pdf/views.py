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
    success_url = "merge"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form,
                   'button': 'Juntar PDF'}
        return render(request, self.template_name, context)

    def post(self, request):
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
        context = {'form': form,
                   'button': 'Juntar PDF'}
        return render(request, self.template_name, context=context)



