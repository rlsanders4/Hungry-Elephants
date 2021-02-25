#!/usr/bin/env python
import _thread
from gpiozero import LED
import time

# the delay between triggers in second
delay = 2
# Duration of each on signal
duration = 1

# Define a function for the pin thread
def aktivieren(fs):
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

for feederStatus in feederStatuses:
    if feederStatus[0] != '#':
        fs = feederStatus.strip("\n").split(",")
        if fs[3] == "BUZY":
            _thread.start_new_thread(aktivieren,(fs,))
            
        