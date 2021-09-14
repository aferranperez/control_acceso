import cv2
import numpy as np
import time
import os
from PIL import Image

#listado de personas a identificar
personas = ["Ferran","Joel","Gabriel","Daniela","Mairelis","Mayra"]


#Esta funcion utiliza la webcam para adquirir caras
def clasificar_rostros_webcam():
    #Antes de clasificar entrenamos
    reconocedor = Entrenar()
   
    #reconocedor = cv2.face.LBPHFaceRecognizer_create()
    #reconocedor.read("modelo.xml")

    #Crear instancia de captura de video
    #cv2.namedWindow("Deteccion facial")
    cap = cv2.VideoCapture(0)
    #capturar el primer fotograma
    if cap.isOpened():
        rval, frame = cap.read()
    else:
        rval = False

    while rval:
        caras, gray = detectar_caras(frame)

        if caras is not None:
            for cara in caras:
                (x, y, w, h) = cara
                face = gray[y:y + w, x:x + h]
                label = reconocedor.predict(face)

                if label is not None:
                    label_text = personas[label[0]]

                    # Pintar el rectangulo
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    # Poner texto
                    cv2.putText(frame, label_text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0),2)



        #muestro el frame resultante de el proceso
        cv2.imshow('img', frame)
        key = cv2.waitKey(5) #ver que hace???

        if key > 0:
            cv2.destroyAllWindows()
            for i in range(1, 5):
                cv2.waitKey(1)
            return
        time.sleep(0.05)
        rval, frame = cap.read()
    return



#Esta funcion devuelve las caras
def detectar_caras(imagen):
    #cargar el clasificador
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    #detectando caras en escala de grises
    caras = face_cascade.detectMultiScale(gris, scaleFactor=1.2, minNeighbors=3)

    #Si no se detectan caras en la imagen devolvemos esto
    if(len(caras) == 0 ):
        return None, None

    #devuelvo donde esta la cara
    return caras, gris

#Hace lo mismo q detectar caras pero solamente lo hace para una sola cara
#porque en el entrenamiento nada mas hay una sola cara a detectar
def detectar_caras_para_entrenamiento(imagen):
    #cargar el clasificador
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    #detectando caras en escala de grises
    caras = face_cascade.detectMultiScale(gris, scaleFactor=1.2, minNeighbors=3)

    #Si no se detectan caras en la imagen devolvemos esto
    if(len(caras) == 0 ):
        return None,None

    #Extraemos el area de la cara
    (x,y,w,h) = caras[0]

    #devuelvo donde esta la cara
    return gris[y:y+w, x:x+h], caras[0]

#Devuelve las caras con sus nombres
def preparar_datos_de_entrenamiento(ruta):  #En esta funcion llama a detectar_caras(imagen)
    #Obtener la lista de los directorios
    directorios = os.listdir(ruta)

    #lista para las cara
    caras = []

    #lista para los nombres
    labels = []

    #Recorremos la lista de directorios
    for nombreDire in directorios:

        label = int(nombreDire)

        #contruimos la ruta del directorio de cada persona
        rutaDirectorioPersona = ruta + "/" + nombreDire

        #obtenemos las imagenes de cada sujeto
        listaImagenesPersona = os.listdir(rutaDirectorioPersona)

        #recorremos las imagenes de cada carpeta
        for nombreImagen in listaImagenesPersona:
            rutaImagen = rutaDirectorioPersona + "/" + nombreImagen

            #leer imagen
            imagen = cv2.imread(rutaImagen)

            #rescalo las imagens
            imagen = cv2.resize(imagen, None, fx=0.6, fy=0.6)

            #detectar cara
            face, rect = detectar_caras_para_entrenamiento(imagen)

            if rect is not None:
                (x, y, w, h) = rect
                # Pintar el rectangulo
                cv2.rectangle(imagen, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # mostrar la imagen
            cv2.imshow("Entrenando..........", imagen)
            cv2.waitKey(100)

            #agregamos las caras detectadas a las lista de imagenes y de etiquetas
            if face is not None:
                caras.append(face)
                labels.append(label)

    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()

    return caras, labels

#Entrena y devuelve el reconocedor facial ya entrenado
def Entrenar():
    print("Preparando datos...")
    caras, nombres = preparar_datos_de_entrenamiento("training-data")
    print("Datos preparados")
    print("Total caras: ", len(caras))
    print("Total nombres", len(nombres))

    # creamos el reconocedor de caras
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    # entrenamos el reconocedor
    face_recognizer.train(caras, np.array(nombres))
    face_recognizer.save("modelo.xml")
    return face_recognizer

clasificar_rostros_webcam()
