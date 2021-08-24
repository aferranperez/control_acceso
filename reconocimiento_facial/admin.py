from django.contrib import admin
from django.db import models

# Register your models here.
from .models import *


#Clase para administrar el modelo Persona 
class PersonaModelAdmin(admin.ModelAdmin):
    list_display = ["nombre","apellido", "fecha_creacion_registro", "fecha_actualizacion_registro"]
    list_filter = ["fecha_creacion_registro"]
    search_fields = ["nombre", "apellido"]
    ordering = ["nombre"]
    inlines = [InlineImage]
    #Especifica el modelo del cual se van a sacar todos los valores anteriores
    class Meta:
        model = Persona


admin.site.register(Persona, PersonaModelAdmin)


