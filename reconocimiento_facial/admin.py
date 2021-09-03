from django.contrib import admin
from django.db import models
from shutil import *
import os

# Register your models here.
from .models import *

#Registre acciones aqui
@admin.action(description="Mover imagenes subidas al Dataset")
def mover_images_dataset(modeladmin, request, queryset):
    ficheros = os.listdir("tmp/")

    for obj in queryset:
        for fichero in ficheros:
            dir = "tmp" + "/" + fichero
            dir_dest = str("media/reconocimiento_facial/" + obj.nombre + obj.apellido + "/")
            move(dir, dir_dest)    





#Clase para administrar el modelo Persona 
class PersonaModelAdmin(admin.ModelAdmin):
    list_display = ["nombre","apellido", "fecha_creacion_registro", "fecha_actualizacion_registro"]
    list_filter = ["fecha_creacion_registro"]
    search_fields = ["nombre", "apellido"]
    ordering = ["nombre"]
    inlines = [InlineImage]
    actions = [mover_images_dataset]
   
    #Especifica el modelo del cual se van a sacar todos los valores anteriores
    class Meta:
        model = Persona

admin.site.register(Persona, PersonaModelAdmin)

