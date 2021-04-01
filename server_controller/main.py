# Server-side controller
# main.py

# python library imports
import sys
import time
import threading

print("####################\n##### Upstream controller starting...")

# get cmd line arg
CLEAN, CLEAN_HARD, VERBOSE, SUPPRESS, DUMMY = False, False, False, False, False
for arg in sys.argv:
    if(arg == "-c" or arg == "--clean"):
        CLEAN = True
    elif(arg == "-ch" or arg == "--cleanhard"):
        CLEAN_HARD = True
    elif(arg == "-v" or arg == "--verbose"):
        VERBOSE = True
    elif(arg == "-s" or arg == "--suppress"):
        SUPPRESS = True
    elif(arg == "-d" or arg == "-t" or arg == "--test" or arg == "--dummy"):
        DUMMY = True

# set logging mode
if not (VERBOSE or SUPPRESS):
    print("##### Running in normal logging mode.")
elif(VERBOSE):
    print("##### Running in verbose logging mode.")
elif(SUPPRESS):
    print("##### Running without logging.")

if DUMMY:
    print("##### Running in DUMMY mode. This will not attempt to connect to raspberry pis.")

# initialize the django ORM and apps before importing models, also allows importing server_controller modules
from django_setup import initDjango
initDjango()

print("##### DB connection initialized.")
if CLEAN:
    print("##### Cleaning data log state on server. This can potentially create duplicate data in the DB logs.")
elif(CLEAN_HARD):
    print("##### Cleaning data log state on server and database.")

#import server_controller components
from pi_manager.connector import Connector, DummyConnector
from schedules.schedule_builder import ScheduleBuilder
from pi_manager.distributor import Distributor, DummyDistributor
from pi_manager.data_puller import DataPuller, DummyDataPuller
from logger import Logger

from schedules import dummy_data

# import models
from django.contrib.auth.models import User
from adminops.models import Pi
from elephants.models import Schedule, Elephant
from datalog.models import RFIDLogData, FeedingData

# setup dummy data
if DUMMY:
    dummy_data.createDummyData()

# default thread with interruptable wait method
class Thread(threading.Thread):
    interval = 1
    def __init__(this):
        threading.Thread.__init__(this)
        this.stopEvent = threading.Event()
    def wait(this, amount):
        time_elapsed = 0
        while not this.stopEvent.is_set() and time_elapsed < amount:
            time.sleep(Thread.interval)
            time_elapsed += Thread.interval

# schedule distribution thread
class DistributorThread(Thread):
    interval = 2
    def run(this):
        # set up logger
        logger = Logger()
        logger.VERBOSE = VERBOSE
        logger.SUPPRESS = SUPPRESS
        logger.logInfo("Schedule distribution thread started.")
        # set up connector to get pi connections
        if DUMMY:
            connector = DummyConnector(logger)
        else:
            connector = Connector(logger)
        connector.connect_pis()
        pis = connector.get_pis()
        # set up distributor and schedule builder
        if DUMMY:
            distributor = DummyDistributor(pis, logger)
        else:
            distributor = Distributor(pis, logger)
        scheduleBuilder = ScheduleBuilder(distributor, logger)
        while not this.stopEvent.is_set():
             # attempt to build and distribute schedules
            scheduleBuilder.run()
            # verify pi connections and update
            connector.update_connection_status()
            connector.connect_pis()
            distributor.pis = connector.get_pis()
            this.wait(DistributorThread.interval)
        logger.logInfo("Schedule distribution thread stopped.")

# data pulling thread
class DataPullerThread(Thread):
    interval = 10
    def run(this):
        # set up logger
        logger = Logger()
        logger.VERBOSE = VERBOSE
        logger.SUPPRESS = SUPPRESS
        logger.logInfo("Data pulling thread started.")
        # set up connector to get pi connections
        if DUMMY:
            connector = DummyConnector(logger)
        else:
            connector = Connector(logger)
        connector.connect_pis()
        pis = connector.get_pis()
        # set up datapuller
        if DUMMY:
            dataPuller = DummyDataPuller(pis, logger)
        else:
            dataPuller = DataPuller(pis, logger)
        if(CLEAN):
            dataPuller.cleanState()
        elif(CLEAN_HARD):
            dataPuller.cleanState()
            FeedingData.objects.all().delete()
            RFIDLogData.objects.all().delete()
        while not this.stopEvent.is_set():
            # attempt to pull data
            dataPuller.pullCompleted()
            dataPuller.pullLogData()
            # verify pi connections and update
            connector.update_connection_status()
            connector.connect_pis()
            dataPuller.pis = connector.get_pis()
            this.wait(DataPullerThread.interval)
        logger.logInfo("Data pulling thread stopped.")

thread1 = DistributorThread()
thread2 = DataPullerThread()
thread1.start()
thread2.start()

print("##### Controller now running. Enter 'stop' to stop the server-side pi controller.\n####################")

# loop for user input
while(True):
    command = input("")
    if(command=="stop"):
        thread1.stopEvent.set()
        thread2.stopEvent.set()
        break
    else:
        print("Enter 'stop' to stop the program")

print("Stopping...")

# wait for all threads to finish
thread1.join()
thread2.join()

print("Stopped.")