from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'adminops'
urlpatterns = [
    path('', views.index, name='index'),
    path('pisetup', views.pisetup, name='pisetup'),
    path('piedit', views.piedit, name='piedit'),
    path('pilist', views.pilist, name='pilist'),
    path('pidelete', views.pidelete, name='pidelete'),
    path('piedit/feedersetup', views.feedersetup, name='feedersetup'),
    path('piedit/antennasetup', views.antennasetup, name='antennasetup'),
    path('piedit/feederdelete', views.feederdelete, name='feederdelete'),
    path('piedit/antennadelete', views.antennadelete, name='antennadelete'),
]