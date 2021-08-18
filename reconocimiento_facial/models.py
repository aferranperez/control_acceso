from django.db import models
from django.db.models.fields import CharField

# Create your models here.

class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=200)
    departamento = models.CharField(max_length=200)
    fecha_creacion_registro =  models.DateTimeField(auto_now=False, auto_now_add=True)
    fecha_actualizacion_registro = models.DateTimeField(auto_now=True, auto_now_add=False)
    cant_imagenes = models.IntegerField()
    CI = models.CharField(max_length=20)
    edad = models.IntegerField()

    def __str__(self):
        return self.nombre
    
    

class Imagen(models.Model):
    imagen = models.ImageField(upload_to='tmp') #investigarOJOOOOOOOOO

    #Una persona posee varias imagenes (Relacion 1 a muchos)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

