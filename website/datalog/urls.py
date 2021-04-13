from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'datalog'
urlpatterns = [
    path('', views.index, name='index'),
    path('rfiddata', views.index, name='rfiddata'),
    path('feedingdata', views.feedingdata, name='feedingdata'),
    path('RFIDcsv',views.getRfidFile, name = 'RFIDcsv'),
    path('completedTaskcsv',views.getCompletedTaskFile, name = 'completedTaskcsv'),    
]
