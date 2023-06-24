from django.shortcuts import render

def word_index(request):
    return render(request, 'pdf/word.html')

