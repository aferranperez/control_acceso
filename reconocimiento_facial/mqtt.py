import paho.mqtt.client
import json
from .models import *

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

            raspberrys = Raspberry.objects.all()

            
        
        