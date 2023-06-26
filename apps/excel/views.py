from django.http import FileResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from apps.pdf.forms import PdfInput
import tabula as tb
import PyPDF2
import io
import tempfile
import os
import openpyxl
import pandas as pd


class Excel(View):
    template_name = "pdf/excel.html"
    form_class = PdfInput
    success_url = "excel"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form,
                   'button': 'Converter para Excel'}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('files')
            merge = PyPDF2.PdfMerger()
            [merge.append(file) for file in files]
            # Salvar o arquivo temporário PDF
            try:
                with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf:
                    merge.write(temp_pdf.name)

                        # Converter o PDF para CSV
                    with tempfile.NamedTemporaryFile(suffix=".csv") as temp_csv:
                        tb.convert_into(input_path=temp_pdf.name, output_path=temp_csv.name,
                                        output_format='csv', guess=True, pages='all')
                        df = pd.read_csv(temp_csv.name)
                        with tempfile.NamedTemporaryFile(suffix=".xlsx") as temp_excel:
                            df.to_excel(temp_excel.name, index=False)

                        # Configurar a resposta HTTP com o arquivo Excel gerado
                            with open(temp_excel.name, 'rb') as excel_file:
                                response = FileResponse(open(excel_file.name, 'rb'), filename='Arquivo.xlsx')                    
                                return response
                
            except Exception as e:
                messages.error(request, f'Infelizmente não foi possível converter o arquivo:')
                messages.error(request, f'Possíveis causas: Diferentes formatos de tabelas ou arquivo sem tabelas')
            
                context = {'form': form,
                   'button': 'Converter para Excel'}
                return render(request, self.template_name, context)
            
            
            
            
        context = {'form': form,
                   'button': 'Converter para Excel'}
        return render(request, self.template_name, context)