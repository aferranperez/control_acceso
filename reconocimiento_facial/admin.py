from django.contrib import admin
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.urls import path
from shutil import *
import os
from django.core import serializers

# Register your models here.
from .models import *

#Clase para administrar el modelo Persona 
class PersonaModelAdmin(admin.ModelAdmin):
    
    #Modifique metodos de la clase
    def get_urls(self):
        urls = super().get_urls()
        
        my_urls = [
            path('refrescar_tabla/', self.update),
        ]

        return my_urls + urls

    #Registre acciones aqui
    @admin.action(description="Mover imagenes al Dataset del Trabajador")
    def mover_images_dataset(self, request, queryset):
        
        obj_Imgs = Imagen.objects.filter(image__contains="tmp/dataset/")
        ficheros = os.listdir("tmp/dataset/")
        
        if ficheros == []:
            return self.message_user(request,"No hay imágenes pendientes para subir al Dataset",level='error') 

        for persona in queryset:
            for fichero in ficheros:
                dir = str("tmp" + "/" + "dataset" + "/" + fichero)              
                for obj in obj_Imgs:  
                    if dir == obj.image and persona.id == obj.persona_id:
                        model = Persona.objects.filter(id = obj.persona_id)
                        dir_dest = str("media/reconocimiento_facial/" + model[0].nombre + ' ' + model[0].apellido + "/" + str(obj.id) + ".jpg")    
                        move(dir, dir_dest)  
                        obj.image = dir_dest
                        obj.save()
                        
        
        self.message_user(request,"Actualice los Datos para validar cambios",level="info")       

    def update(self, request):
        from re import split
        model_Img = Imagen.objects.all()
        model_Persona = self.model.objects.all()
        
        for persona in model_Persona:
            cont1,cont2 = 0,0
            for imagen in model_Img:
                if imagen.persona_id == persona.id:
                    dir = split("/", str(imagen.image))            
                    if str(dir[0]) == "tmp":
                        cont1+=1             
                        persona.imagenes_sin_subir = cont1
                        persona.save()
                    elif str(dir[0]) == "media":
                        cont2+=1
                        persona.imagenes_sin_subir = cont1
                        persona.imagenes_en_dataset = cont2
                        persona.save()

        self.message_user(request, "Actualizado con exito", level="info")
        return HttpResponseRedirect("../")

    @admin.action(description="Entrenar modelo con trabajadores seleccionados")
    def entrenar_modelo(self, request, queryset): 
        for persona in queryset:
            if persona.imagenes_sin_subir != 0:
                return self.message_user(request, "Hay personas con imágenes pendientes para subida al dataset. Actualice los datos.", level="warning")

            if persona.imagenes_en_dataset < 6:
                return self.message_user(request, "Hay personas seleccionadas con menos de 6 imágenes en dataset para entrenar. Actualice los datos.", level="warning")    
        
        JSON_Serializer = serializers.get_serializer("json")
        json_serializer = JSON_Serializer()
        json_serializer.serialize(queryset)

        with open('tmp/data_personas_entrenar.json', 'w') as jsonfile:
            json_serializer.serialize(queryset, stream=jsonfile)

        return render(request, 'reconocimiento_facial/admin/entrenar_modelo.html', {'model_Persona':queryset})

    #Registre parametros aqui
    list_display = ["nombre","apellido", "fecha_creacion_registro", "fecha_actualizacion_registro", "imagenes_en_dataset", "imagenes_sin_subir"]
    list_filter = ["fecha_creacion_registro"]
    search_fields = ["nombre", "apellido"]
    ordering = ["nombre"]
    inlines = [InlineImage]
    actions = [mover_images_dataset,entrenar_modelo]            
    change_list_template = "reconocimiento_facial/admin/admin.html"


admin.site.register(Persona, PersonaModelAdmin)

