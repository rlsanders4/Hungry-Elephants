from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'datalog'
urlpatterns = [
    path('', views.index, name='index'),
    path('feedingdata', views.feedingdata, name='feedingdata'),
]