from django.contrib import admin
from django.urls import path
from esteganografia import views

urlpatterns = [
    path('', views.esteganografia, name='esteganografia'),
    path('cifrar', views.cifrar, name='cifrar'),
    path('descifrar', views.descifrar, name='descifrar'),
]