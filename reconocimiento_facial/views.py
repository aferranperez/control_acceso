from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'reconocimiento_facial/index.html')