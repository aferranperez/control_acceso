from time import time
from reconocimiento_facial.models import *
import cv2
import numpy as np
from django.core.serializers import deserialize
import datetime
import time
def entrenar_model(Modelo_Img):

    caras, nombres = preparar_datos(Modelo_Img)
    print("Total de caras", len(caras))
    print("Total de nombre", len(nombres))
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(caras, np.array(nombres))

    tt = datetime.date.today().timetuple()
    dir = "modulos_py/face_recognizer/modelos_entrenados/" + str(tt.tm_year) + "-" + str(tt.tm_mon) + "-" + str(tt.tm_mday) + "-" + str(time.time()) + "-" +"modelo.xml"
    
    face_recognizer.save(dir)

    file = str(tt.tm_year) + "-" + str(tt.tm_mon) + "-" + str(tt.tm_mday) + "-" + str(time.time()) + "-" + "modelo"
    modelo = Modelo_Entrenado.objects.create(nombre = file)
    modelo.save()
   
    with open('tmp/data_personas_entrenar.json') as file:
        for obj in deserialize("json", file):
            Miembro_del_Modelo.objects.create(CI = obj.object.CI ,modelo_entrenado = modelo, persona = obj.object).save()  
    

def preparar_datos(Modelo_Img):
    caras = []
    labels = []

    with open('tmp/data_personas_entrenar.json') as file:
        for obj in deserialize("json", file):
            label = int(obj.object.id)
            
            mod_images = Modelo_Img.objects.filter(persona_id = obj.object.id )
            
            for mod_img in mod_images:
                image = cv2.imread(str(mod_img.image))
                image = cv2.resize(image, None, fx=0.6, fy=0.6)

                face, rect = detectar_caras(image)

                if rect is not None:
                    (x, y, w, h) = rect
                    cv2.rectangle(image, (x,y), (x+w, y+h), (255,0,0), 2)

                
                cv2.imshow("Entrenando......", image)
                cv2.waitKey(50)

                if face is not None:
                    caras.append(face)
                    labels.append(label)
    
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()

    return caras, labels

def detectar_caras(image):
    dir = "modulos_py/face_recognizer/haarcascade-xml/haarcascade_frontalface_alt.xml"
    face_cascade = cv2.CascadeClassifier(dir)
    gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    caras = face_cascade.detectMultiScale(gris, scaleFactor=1.2, minNeighbors=3)
    
    if(len(caras) == 0):
        return None, None

    (x,y,w,h) = caras[0]
    return gris[y:y+w, x:x+h], caras[0]