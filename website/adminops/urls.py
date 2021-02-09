from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'adminops'
urlpatterns = [
    path('', views.index, name='index'),
    path('pisetup', views.pisetup, name='pisetup'),
    path('piedit', views.piedit, name='piedit'),
]