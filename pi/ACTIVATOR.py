#!/usr/bin/env python3
from threading import Thread 
from gpiozero import LED
import time
import os
import sys

# the delay between triggers in second
delay = 2
# Duration of each on signal
duration = 1

# only allow one ACTIVATOR running
if os.popen("pgrep -a python | grep 'ACTIVATOR.py'").read().count('\n') > 1:
    # This means there are already an instence running.
    sys.exit("\nOnly one ACTIVATOR instence can be executed at the same time!\n")

# Define a function for the pin thread
def aktivieren(fs):
    print('Executing: '+ fs[4])
    filename = '/home/pi/rawdata/tasks_running/PIN' + fs[2] + '.todo'
    with open(filename, "r") as f:
        commands = f.readlines()
    taskFound = False
    for command in commands:
        if command[0] != '#':
            cmd = command.strip("\n").split(",")
            if not (cmd[0] == fs[0] and cmd[1] == fs[1] and cmd[2] == fs[2] and cmd[3] == fs[4]):
                print("PIN task include extra lines, discarding: ",command)
            else:
                taskFound = True
                triggerPin(cmd)
                break
    if not taskFound:
        print("PIN file and Feeder Status file content inconsistent! Clearing file...")
    # clears the file after the task is done
    open(filename, "w").close()
    print('PIN ',fs[2],' finished executing')

# Trigger the commanded pin
def triggerPin(cmd):
    pin = LED(int(cmd[2]))
    for i in range(int(cmd[4])):
        print('PIN ', cmd[2] ,' is on!')
        pin.on()
        time.sleep(duration)
        pin.off()
        time.sleep(delay)
    
    
feederStatusFile = '/home/pi/shared_data/feeder.status'


with open(feederStatusFile, "r") as f:
    feederStatuses = f.readlines()

threads = []
for feederStatus in feederStatuses:
    if feederStatus[0] != '#':
        fs = feederStatus.strip("\n").split(",")
        if fs[3] == "BUZY":
            thread = Thread(target = aktivieren, args = (fs, ))
            thread.start()
            threads.append(thread)

for thread in threads:
    thread.join()

print('Job done!')
            
            
        