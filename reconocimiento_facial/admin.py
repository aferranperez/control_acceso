from django.contrib import admin
from django.shortcuts import render,HttpResponseRedirect
from django.urls import path
from shutil import *
from django.core import serializers
from paho.mqtt.client import Client
from .mqtt import *
from .network import *

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
    
    #def has_delete_permission(self, request, obj = None):
    #    return False

#Clase para administrar el modelo de Raspberry
class RaspberryModelAdmin(admin.ModelAdmin):
    
    MQTT_SERVER = "192.168.56.100"
    
    client = Client(client_id="admin", clean_session=False, transport="tcp")
    client.on_message = on_message 

    #Modifique metodos de la clase
    def get_urls(self):
        urls = super().get_urls()  
        my_urls = [
            path("actualizar_estado/", self.actualizar_estado),
        ]
        return my_urls + urls

    def actualizar_estado(self,request):
        payload = {
            'action' : 'get_state',
        }
        
        publish_suscribe_config(self,payload,self.client,self.MQTT_SERVER,request)
        
        return HttpResponseRedirect("../")

    @admin.action(description="Sincronizar dispositivo /s")
    def syncronize_devices(self, request, queryset):
        payload = {
            'action' : 'syncronize',
            'devices': '%s' %str({raspberry.ip_address for raspberry in queryset}),      
        }
        
        print(payload['devices'])
        publish_suscribe_config(self,payload,self.client,self.MQTT_SERVER,request)
    
    @admin.action(description="Cargar modelo a dispositivo /s seleccionado /s")
    def load_model(self, request, queryset):
        
        #for raspberry in queryset:
        model_face = Modelo_Entrenado.objects.get(id = queryset[0].modelo_id)

        payload = {
            'action' : 'load_model',
            'data':{
                'ip_destino': '%s' %queryset[0].ip_address ,
                'model_id' : '%s' %model_face.id ,
                'model_name' : '%s' %model_face.nombre,
            }
        }
        print("Preparando paquete a enviar por MQTT...")
        print(payload)
        publish_suscribe_config(self,payload,self.client,self.MQTT_SERVER,request)
        
        return


    #Registre parametros aqui
    list_display = ["nombre","ubicacion","is_syncronize","is_active","have_model","ip_address","id_suscribe"]
    list_filter = ["is_active","have_model"]
    search_fields = ["nombre"]
    ordering = ["nombre"]
    actions = [syncronize_devices, load_model]
    change_list_template = ["reconocimiento_facial/admin/raspberry_changelist.html"]

admin.site.register(Persona, PersonaModelAdmin)
admin.site.register(Modelo_Entrenado, ModelosEntrenadosAdmin)
admin.site.register(Raspberry, RaspberryModelAdmin)
