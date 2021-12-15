from time import sleep
import paho.mqtt.client
import json
from .models import *
from .network import Socket_IoT
from django.contrib import admin
import socket

def on_message(client, userdata, message):

    #Para analizar las respuestas de las Raspberry a las configuraciones
    if message.topic == "config_device/answer/":   
        
        payload_decode = json.loads(message.payload)
        
        if payload_decode['action'] == "respond_state":
            print("-------------------")
            print('topic: %s' % message.topic)
            print('payload: %s' % message.payload)
            print('qos: %s' % message.qos)
            print(payload_decode['data'])

        elif payload_decode['action'] == "respond_syncronize":
            pass
        
        elif payload_decode['action'] == "respond_load_model":
            ip_address = payload_decode['data']['ip_address']
            port = payload_decode['data']['port']
            
            print(f'Dispositivo {ip_address}:{port} solicitando carga de modelo')

            conexion = Socket_IoT()
            
            try:
                with socket.create_connection((ip_address, port)) as conn:
                    #dir = "modulos_py/face_recognizer/modelos_entrenados/2021-9-20-1632117746.97755-modelo.xml"
                    dir = "modulos_py/face_recognizer/modelos_entrenados/" + payload_decode['data']['model_name'] + ".xml"

                    print(f'Conectado al servidor {ip_address}:{port}')
                    print("Conectado")
                    print(f"Enviando modelo localizado en: {dir} ...")
                    print("Enviando modelo...")
                    conexion.send_file(conn, dir)
                    print("Enviado.")
                    
            except Exception as e:
                print(e)
            else:
                pass


def publish_suscribe_config(self,payload,client,MQTT_SERVER,request):

    try:
        client.connect(MQTT_SERVER, port= 1883, keepalive=5) 
            
    except Exception as e:
        error = 'Ha ocurrido un error de %s' % e
        self.message_user(request, str(error) , level="error")
        
    else:
        payload = json.dumps(payload)
        
        client.publish(topic="config_device/", payload= payload, qos=0)         
            
        client.subscribe("config_device/answer/", qos=0)
        client.loop_start()          
        sleep(5)    #doy 5 segundos para que todos los dispositivos actualicen
        self.message_user(request, "Completado con exito") 
        client.loop_stop()
        

        