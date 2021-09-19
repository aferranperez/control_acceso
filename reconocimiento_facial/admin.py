from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from shutil import *
from django.core import serializers

# Register your models here.
from .models import *

#Clase para administrar el modelo Persona 
class PersonaModelAdmin(admin.ModelAdmin):
    
    #Modifique metodos de la clase
    def get_urls(self):
        urls = super().get_urls()  
        my_urls = [

        ]
        return my_urls + urls

    #Registre acciones aqui
    
    @admin.action(description="Entrenar modelo con trabajadores seleccionados")
    def entrenar_modelo(self, request, queryset): 
        for persona in queryset:
            if persona.imagenes_en_dataset < 10:
                return self.message_user(request, "Hay personas seleccionadas con menos de 10 imágenes en dataset para entrenar. Actualice los datos.", level="warning")    
        
        JSON_Serializer = serializers.get_serializer("json")
        json_serializer = JSON_Serializer()
        json_serializer.serialize(queryset)

        with open('tmp/data_personas_entrenar.json', 'w') as jsonfile:
            json_serializer.serialize(queryset, stream=jsonfile)

        return render(request, 'reconocimiento_facial/admin/entrenar_modelo.html', {'model_Persona':queryset})

    #Registre parametros aqui
    list_display = ["nombre","apellido", "fecha_creacion_registro", "fecha_actualizacion_registro", "imagenes_en_dataset"]
    list_filter = ["fecha_creacion_registro"]
    search_fields = ["nombre", "apellido"]
    ordering = ["nombre"]
    inlines = [InlineImage]
    actions = [entrenar_modelo]            
    change_list_template = "reconocimiento_facial/admin/admin.html"

#Clase para administrar el modelo de Modelos_Entrenados
class ModelosEntrenadosAdmin(admin.ModelAdmin):
    #Registre parametros aqui
    list_display = ["nombre","fecha_creacion"]
    search_fields = ["nombre"]
    ordering = ["fecha_creacion"]
    inlines = [InLineMiembros]
    list_filter = ["fecha_creacion"]

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj = None):
        return False

admin.site.register(Persona, PersonaModelAdmin)
admin.site.register(Modelo_Entrenado, ModelosEntrenadosAdmin)
