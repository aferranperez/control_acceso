from os import name
from django.urls import path
from . import views

app_name = 'reconocimiento_facial'
urlpatterns = [
    path('',views.index, name='index'),
    path('entrenar_modelo/', views.entrenar_modelo, name='entrenar_modelo'),
]