import io
import tempfile
import PyPDF2
from django.http import FileResponse
from django.shortcuts import render
from django.views.generic import View
import pandas as pd
from apps.pdf.forms import PdfInput
import pdf2docx
import tabula as tb
from django.contrib import messages

class Word(View):
    template_name = "pdf/word.html"
    form_class = PdfInput
    success_url = "word"

    def get(self, request):
        form = self.form_class()
        context = {'form': form,
                   'button': 'Converter para Word'}
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
            try:
                with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf:
                    merge.write(temp_pdf.name)
                    with tempfile.NamedTemporaryFile(suffix='.docx') as temp_word:
                        self.convert_pdf_to_word(temp_pdf.name, temp_word.name)
                        with open(temp_word.name, 'rb') as file_word:
                            word_data = file_word.read()
                            # Configurar a resposta HTTP com o arquivo Word gerado
                            response = FileResponse(io.BytesIO(word_data), filename='Arquivo.docx')
                            return response
                
            except Exception as e:
                messages.error(request, f'Infelizmente não foi possível converter o arquivo:\n{e}')
        context = {'form': form,
                   'button': 'Converter para Word'}
        return render(request, self.template_name, context)


    def convert_pdf_to_word(self, pdf_path, docx_path):
        conversor = pdf2docx.Converter(pdf_path)
        conversor.convert(docx_path)
        conversor.close


   



        
