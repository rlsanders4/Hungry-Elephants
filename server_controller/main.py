# Server-side controller
# main.py

# initialize the django ORM and apps before importing models
from django_setup import initDjango
initDjango()

# import models
from django.contrib.auth.models import User
from adminops.models import Pi

for user in User.objects.all():
    print(user.username)

for pi in Pi.objects.all():
     print(pi.name)