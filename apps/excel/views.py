from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from apps.pdf.forms import PdfInput
import tabula as tb
import PyPDF2
import io
import tempfile
import os


class Excel(View):
    template_name = "pdf/excel.html"
    form_class = PdfInput
    success_url = "excel"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('files')

            options = {
                        "pages": "all",  # Converter todas as páginas
                    }
            merge = PyPDF2.PdfMerger()
            [merge.append(file) for file in files]
            
             # Salvar o arquivo temporário
            with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf:
                merge.write(temp_pdf.name)

                # Converter o PDF para Excel
                with tempfile.NamedTemporaryFile(suffix=".csv") as temp_excel:
                    tb.convert_into(temp_pdf.name, temp_excel.name, output_format="csv", **options)

                    # Configurar a resposta HTTP com o arquivo Excel gerado
                    with open(temp_excel.name, 'rb') as excel_file:
                        response = HttpResponse(excel_file.read(), content_type='application/vnd.ms-excel')
                        response['Content-Disposition'] = 'attachment; filename="arquivo.xlsx"'

                    # Remover o arquivo temporário
                    os.remove(temp_excel.name)

                    return response

        return render(request, self.template_name, {'form': form})