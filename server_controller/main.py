# Server-side controller
# main.py

# initialize the django ORM and apps before importing models
from django_setup import initDjango
initDjango()

import time

# import models
from django.contrib.auth.models import User
from adminops.models import Pi

for user in User.objects.all():
    print(user.username)

for pi in Pi.objects.all():
     print(pi.name)


#initialize distributor, schedule builder, and connector

#start main loop w/ schedule builder and connector
#get schedules, get pi connections, then send those pi connections to the distributor
#lastly, send the schedules to the distributor to handle file transfer in distributor thread