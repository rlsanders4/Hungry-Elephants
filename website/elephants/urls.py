from django.urls import path

from . import views

#be sure to give every path a name variable so when we create links in the html templates we can reference these urls
urlpatterns = [
    path('', views.index, name='index'),
]