from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('entrenar_modelo/<str:estado>/', views.entrenar_modelo, name='entrenar_modelo'),
]