from time import sleep
from django.contrib import admin
from django.shortcuts import render,HttpResponseRedirect
from django.urls import path
from shutil import *
from django.core import serializers
from paho.mqtt.client import Client



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
    
    def has_delete_permission(self, request, obj = None):
        return False

#Clase para administrar el modelo de Raspberry
class RaspberryModelAdmin(admin.ModelAdmin):
    ip_broker = str("192.168.56.100")
    client = Client(client_id="admin", clean_session=False, transport="tcp")
    
    #Modifique metodos de la clase
    def get_urls(self):
        urls = super().get_urls()  
        my_urls = [
            path("actualizar_estado/", self.actualizar_estado),
        ]
        return my_urls + urls

    def actualizar_estado(self,request):
        from .mqtt import on_message
        import json
             
        self.client.on_message = on_message 
        
        payload = {
            'action' : 'get_state',
        }

        try:
            self.client.connect(self.ip_broker, port= 1883, keepalive=10) 
            
        except Exception as e:
            error = 'Ha ocurrido un error de %s' % e
            self.message_user(request, str(error) , level="error")
        
        else:
            payload = json.dumps(payload)
            self.client.publish(topic="config_device/", payload= payload, qos=1)         
            
            self.client.subscribe("config_device/answer/", qos=1)
            self.client.loop_start()          
            sleep(5)    #doy 5 segundos para que todos los dispositivos actualicen
            self.message_user(request, "Actualización con exito") 
        
        finally:
            self.client.loop_stop()
            return HttpResponseRedirect("../")

        
        
    @admin.action(description="Enviar mensaje a esa Raspberry")
    def mensaje_MQTT(self, request, queryset):
        from paho.mqtt import publish

        publish.single("prueba/", payload="EXCELENTE", qos=2, retain=False, hostname="192.168.56.100", port=1883, transport="tcp")

    
    #Registre parametros aqui
    list_display = ["nombre","ubicacion","is_active","is_synchronized","have_model","ip_address","id_suscribe"]
    list_filter = ["is_active","is_synchronized","have_model"]
    search_fields = ["nombre"]
    ordering = ["nombre"]
    actions = [mensaje_MQTT]
    change_list_template = ["reconocimiento_facial/admin/raspberry_changelist.html"]
        
          
admin.site.register(Persona, PersonaModelAdmin)
admin.site.register(Modelo_Entrenado, ModelosEntrenadosAdmin)
admin.site.register(Raspberry, RaspberryModelAdmin)
