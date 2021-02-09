from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'datalog'
urlpatterns = [
    path('/', views.base, name='base'),
]