from django.contrib import admin

# Register your models here.
from .models import Persona

#Clase para administrar el modelo Persona 
class PersonaModelAdmin(admin.ModelAdmin):
    list_display = ["nombre","apellido", "fecha_creacion_registro", "fecha_actualizacion_registro"]
    list_filter = ["fecha_creacion_registro"]
    search_fields = ["nombre", "apellido"]
    ordering = ["nombre"]
    
    #Especifica el modelo del cual se van a sacar todos los valores anteriores
    class Meta:
        model = Persona

admin.site.register(Persona, PersonaModelAdmin)

