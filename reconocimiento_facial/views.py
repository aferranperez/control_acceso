from django.shortcuts import render
from .models import Persona,Imagen
from django.core.serializers import deserialize

# Create your views here.
def index(request):
    return render(request, 'reconocimiento_facial/index.html')


def entrenar_modelo(request):
    from modulos_py.face_recognizer import entrenar
    entrenar.entrenar_model(Imagen)
    estado = 'ya estoy entrenando'
    return render(request, 'reconocimiento_facial/admin/entrenar_modelo.html', {'estado':estado})

