from django.contrib import admin
from django.db import models
from shutil import *
import os

# Register your models here.
from .models import *



#Clase para administrar el modelo Persona 
class PersonaModelAdmin(admin.ModelAdmin):
   
    #Registre acciones aqui
    @admin.action(description="Mover imagenes subidas al Dataset")
    def mover_images_dataset(self, request, queryset):
        
        obj_Imgs = Imagen.objects.filter(image__contains="tmp/")
        ficheros = os.listdir("tmp/")
        
        for fichero in ficheros:
            dir = str("tmp" + "/" + fichero)
            
            for obj in obj_Imgs:  
                if dir == obj.image:
                    model = Persona.objects.filter(id = obj.persona_id)
                    dir_dest = str("media/reconocimiento_facial/" + model[0].nombre + ' ' + model[0].apellido + "/" + fichero)    
                    move(dir, dir_dest)  
                    obj.image = dir_dest
                    obj.save()
            

    #Registre parametros aqui
    list_display = ["nombre","apellido", "fecha_creacion_registro", "fecha_actualizacion_registro"]
    list_filter = ["fecha_creacion_registro"]
    search_fields = ["nombre", "apellido"]
    ordering = ["nombre"]
    inlines = [InlineImage]
    actions = [mover_images_dataset]            

admin.site.register(Persona, PersonaModelAdmin)

