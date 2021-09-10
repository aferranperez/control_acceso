from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'reconocimiento_facial/index.html')

def entrenar_modelo(request):
    return render(request, 'reconocimiento_facial/admin/entrenar_modelo.html')