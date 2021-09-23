from abc import abstractclassmethod
from django.db import models
from django.contrib import admin
from django.db.models.deletion import CASCADE
import os

from django.db.models.fields import CharField

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
    imagenes_en_dataset = models.PositiveIntegerField(editable=False, default=0)

    class Meta:
        verbose_name_plural = "Trabajadores del Centro"
        

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
                        obj.save()
        else:
            folder = 'media/reconocimiento_facial/' + self.nombre +' '+ self.apellido   
            if not os.path.exists(folder):
                os.mkdir(str(folder))
        
        super(Persona, self).save()
        
    def __str__(self):
        return '%s %s' % (self.nombre, self.apellido)

  
class Imagen(models.Model):
    
    def persona_directory_path(instance,filename):
        return 'media/reconocimiento_facial/{0} {1}/{2}'.format(instance.persona.nombre, instance.persona.apellido, filename)
      
    def save(self):
        persona = Persona.objects.get(id = self.persona_id)
        
        if persona:
            persona.imagenes_en_dataset += 1
            persona.save()

        super(Imagen, self).save()
        
    def delete(self):
        persona = Persona.objects.get(id = self.persona_id)

        if persona:
            persona.imagenes_en_dataset -= 1
            persona.save()
        
        super(Imagen, self).delete()

    persona = models.ForeignKey(Persona, on_delete=CASCADE)
    image = models.ImageField(upload_to= persona_directory_path)

class InlineImage(admin.TabularInline):
    model = Imagen

class Modelo_Entrenado(models.Model):
    nombre = models.CharField(max_length= 50, editable=False)
    fecha_creacion = models.DateTimeField(auto_now=False, auto_now_add=True)
    trabajadores = models.ManyToManyField(
        Persona,
        through='Miembro_del_Modelo',
        through_fields=('modelo_entrenado', 'persona'), 
    ) 
    class Meta:
        verbose_name_plural = "Modelos Entrenados"

    
    def __str__(self):
        return self.nombre

class Miembro_del_Modelo(models.Model):
    CI = models.CharField(max_length=20, blank=True, editable= False)
    modelo_entrenado = models.ForeignKey(Modelo_Entrenado, models.SET_NULL, blank=True, null=True,)
    persona = models.ForeignKey(Persona, models.SET_NULL, blank=True, null=True,)

    class Meta:
        verbose_name_plural = "Miembros del Modelo"

    def __str__(self):
        return 'Carnet de Identidad : %s' % (self.CI)

class InLineMiembros(admin.TabularInline):
    model = Miembro_del_Modelo


class Raspberry(models.Model):
    UBICACIONES_CHOICES = (
        ('Entrada', 'Entrada'),
        ('Comedor', 'Comedor'),
        ('Taller', 'Taller'),
    )
    
    nombre = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=50, choices= UBICACIONES_CHOICES)
    is_active = models.BooleanField(default=False, editable=False)
    is_synchronized = models.BooleanField(default=False, editable=False)
    have_model = models.BooleanField(default=False, editable=False)
    ip_address = models.GenericIPAddressField()

    modelo = models.OneToOneField(Modelo_Entrenado, models.SET_NULL, blank= True, null=True)

    class Meta:
        verbose_name_plural = "Raspberrys_Cámaras"
    
    def __str__(self):
        return self.nombre