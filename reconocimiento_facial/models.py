from abc import abstractclassmethod
from django.db import models
from django.contrib import admin
from django.db.models.deletion import CASCADE


# Create your models here.

class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=200)
    departamento = models.CharField(max_length=200)
    fecha_creacion_registro =  models.DateTimeField(auto_now=False, auto_now_add=True)
    fecha_actualizacion_registro = models.DateTimeField(auto_now=True, auto_now_add=False)
    CI = models.CharField(max_length=20)
    edad = models.IntegerField()

    #Sobrescribimos el metodo save para que cree la carpeta del dataset de cada persona
    def save(self):
        import os
        folder = 'media/reconocimiento_facial/' + self.nombre +' '+ self.apellido
        
        if not os.path.exists(folder):
            os.mkdir(str(folder))
        
        super(Persona, self).save()

    def __str__(self):
        return self.nombre


class Imagen(models.Model):
    persona = models.ForeignKey(Persona, on_delete=CASCADE)
    image = models.ImageField(upload_to='tmp/')


class InlineImage(admin.TabularInline):
    model = Imagen

