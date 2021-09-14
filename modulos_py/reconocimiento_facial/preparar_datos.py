import os

def preparar_datos_para_entrenamiento(ruta):
    dir_personas = os.listdir(ruta)
    caras = []
    labels = []

    for persona in dir_personas:
        label = str(persona)

        ruta_dir_persona = ruta + "/" + persona
        ruta_dir_images = os.listdir(ruta_dir_persona)

        print(ruta_dir_persona)

        for imagen in ruta_dir_images:
            ruta_image = ruta_dir_persona + "/" + imagen
            print(ruta_image)
    