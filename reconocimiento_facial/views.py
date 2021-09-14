import json
from django.shortcuts import render
from .models import Persona
from django.core.serializers import deserialize
import json
# Create your views here.
def index(request):
    return render(request, 'reconocimiento_facial/index.html')


def entrenar_modelo(request, estado):
    from modulos_py.reconocimiento_facial.preparar_datos import preparar_datos_para_entrenamiento
    
    if estado == "entrenamiento_parcial":
        with open('tmp/data_personas_entrenar.json') as file:
            for obj in deserialize("json", file):
                print(obj.object.id)


    ruta = "media/reconocimiento_facial"
    preparar_datos_para_entrenamiento(ruta)
    estado = 'ya estoy entrenando'
    return render(request, 'reconocimiento_facial/admin/entrenar_modelo.html', {'estado':estado})