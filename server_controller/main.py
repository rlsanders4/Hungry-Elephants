# Server-side controller
# main.py

# initialize the django ORM and apps before importing models
from django_setup import initDjango
initDjango()

from pi_manager.connector import Connector, DummyConnector
from schedules.schedule_builder import ScheduleBuilder
from pi_manager.distributor import Distributor, DummyDistributor

import time
import threading

from schedules import dummy_data

# import models
from django.contrib.auth.models import User
from adminops.models import Pi
from elephants.models import Schedule, Elephant

for user in User.objects.all():
    print(user.username)

for pi in Pi.objects.all():
     print(pi.name)

for schedule in Schedule.objects.all():
    print(schedule.name)

dummy_data.createDummyData()

#initialize distributor, schedule builder, and connector

#start main loop w/ schedule builder and connector
#get schedules, get pi connections, then send those pi connections to the distributor
#lastly, send the schedules to the distributor to handle file transfer in distributor thread

running = True

def run():
    connector = Connector()
    connector.connect_pis()
    pis = connector.get_pis()
    distributor = Distributor(5, pis)
    scheduleBuilder = ScheduleBuilder(5, distributor)
    while(running):
        
        scheduleBuilder.run()

thread = threading.Thread(target=run, args=())
thread.start()

print("Enter 'stop' to stop the server controller")
while(True):
    command = input("")
    if(command=="stop"):
        running = False
        break
    else:
        print("Enter 'stop' to stop the program")

thread.join()

dummy_data.clearDummyData()

