from abc import abstractclassmethod
from django.db import models
from django.contrib import admin
from django.db.models.deletion import CASCADE
import os

# Create your models here.

class Persona(models.Model):
    DEPARTAMENTO_CHOICES = (
        ('Software', 'Software'),
        ('AudioVisual', 'AudioVisual'),
        ('Taller', 'Taller'),
    )

    nombre = models.CharField(max_length=50, blank=False)
    apellido = models.CharField(max_length=200, blank=False)
    departamento = models.CharField(max_length=100, choices=DEPARTAMENTO_CHOICES)
    fecha_creacion_registro =  models.DateTimeField(auto_now=False, auto_now_add=True)
    fecha_actualizacion_registro = models.DateTimeField(auto_now=True, auto_now_add=False)
    CI = models.CharField(max_length=20, blank=False)
    edad = models.PositiveIntegerField()
    imagenes_en_dataset = models.PositiveIntegerField(editable=False, default='0')
    imagenes_sin_subir = models.PositiveIntegerField(editable=False, default='0')


    class Meta:
        verbose_name_plural = "Trabajadores"
        


    #Sobrescribimos el metodo save para que cree la carpeta del dataset de cada persona
    def save(self):
        persona = Persona.objects.filter(id = self.id) 
        
        if persona.exists(): #estoy editando la persona
            if persona[0].nombre != self.nombre or persona[0].apellido != self.apellido:

                folder = 'media/reconocimiento_facial/' + persona[0].nombre +' '+ persona[0].apellido
                new_folder = 'media/reconocimiento_facial/' + self.nombre +' '+ self.apellido
                
                if os.path.exists(folder):
                    os.rename(folder, new_folder)
                
                images = Imagen.objects.filter(persona_id = self.id, image__contains = 'media/reconocimiento_facial/')
                if images.exists():
                    from re import split
                    for obj in images:
                        name_file = str(split("/", str(obj.image))[3])
                        obj.image = new_folder + '/' + name_file
                        print(obj.image)
                        obj.save()

        else:
            folder = 'media/reconocimiento_facial/' + self.nombre +' '+ self.apellido   
            if not os.path.exists(folder):
                os.mkdir(str(folder))
        
        super(Persona, self).save()
        
    def __str__(self):
        return self.nombre

class Imagen(models.Model):
    persona = models.ForeignKey(Persona, on_delete=CASCADE)
    image = models.ImageField(upload_to='tmp/dataset')
 
class InlineImage(admin.TabularInline):
    model = Imagen
