#!/usr/bin/env python
import os
import sys
import time
import datetime
from configparser import ConfigParser

# PANIC!

feederStatusFileName = "/home/pi/shared_data/feeder.status"
pinTODOFolderName = "/home/pi/rawdata/tasks_running"

keepFile = False
if len(sys.argv) > 1:
    # Some arguments had been passed in. We conly interest in the first one.
    if sys.argv[1] == '-kf' or sys.argv[1] == '--keep_file':
        keepFile =True
        print('Keeping files!')
    else:
        print('Usage: sudo python3 BIG_RED_STOP_BUTTON.py')
        print('-kf  --keep_file  not clearing files')
        print('-h  --help  display this message')


# still only admin can run as for requirement cleaning up services
if not os.geteuid() == 0:
    sys.exit("\nOnly root can run this script\n")

# This file will:
# Read the config file, then stop everything that is running and reset programs and files to an execution ready state (not initialized)

now = datetime.datetime.now()
startTime = time.time()
print ('STOP and cleaning everything! Now is '+ now.strftime('%Y-%m-%d %H:%M:%S'))


# stopping initializer
os.system("systemctl daemon-reload")
print('Stopping and cleaning initializer service...')
os.system("systemctl stop initializer && systemctl disable initializer")
os.system('sudo rm /etc/systemd/system/initializer.service')
os.system('sudo pkill -9 -f initializer.py')
    
# ----------------------------------------------------
# set up the system according to config file

config_object = ConfigParser()
config_object.read("/home/pi/shared_data/config.ini")
for site in config_object.sections():
    site = config_object[site]
    siteName = site['SITE_CODE']+"_serialLogger"
    print('Stopping and cleaning '+siteName+' service...')
    os.system("systemctl stop "+siteName+" && systemctl disable "+siteName)
    os.system('sudo rm /etc/systemd/system/'+siteName+'.service')

            
            
# Stopping all python scripts
print('Killing all running serial loggers...')
os.system('sudo pkill -9 -f serialLogger.py')
print('Killing all running controllers...')
os.system('sudo pkill -9 -f controller.py')
print('Killing all running actovators...')
os.system('sudo pkill -9 -f ACTIVATOR.py')
print('Killing all running image creators...')
os.system('sudo pkill -9 -f createImage.sh')
# now we had dealt with the serial logger, we just need to make sure the feeders are right.
# Nuke them
if not keepFile:
    print('Cleaning files...')
    print('Removing all PIN todo files...')
    os.system('sudo rm /home/pi/rawdata/tasks_running/PIN*.todo')
    os.system('sudo rm /home/pi/rawdata/tasks_running/PIN*.temp')
    print('Clearing RFID status file...')
    os.system('sudo cp /dev/null /home/pi/rawdata/rfidstatus.txt')
    print('Clearing feeder status file...')
    os.system('sudo cp /dev/null /home/pi/shared_data/feeder.status')
