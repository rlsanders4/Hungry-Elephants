#!/usr/bin/env python
import os
import sys
from configparser import ConfigParser
from netifaces import interfaces, ifaddresses, AF_INET
import time
import datetime
import filecmp 



feederStatusFileName = "/home/pi/shared_data/feeder.status"
pinTODOFolderName = "/home/pi/rawdata/tasks_running"
# second for controller to execute before ACTIVATOR starts running
executionDelay = 0.5
# second for next epoch starts running
endDelay = 0.5
# Hour to restart every day in 24 hour
restartHour = 4

demomode = False
noLogger = False

if os.popen("pgrep -a python | grep 'initializer.py'").read().count('\n') > 1:
    # This means there are already an instence running.
    sys.exit("\nOnly one instence can be executed at the same time!\n")

if len(sys.argv) > 1:
    # Some arguments had been passed in. We conly interest in the first one.
    if sys.argv[1] == '-d' or sys.argv[1] == '--demo':
        demomode =True
        print('Demoing!')
    elif sys.argv[1] == '-nl' or sys.argv[1] == '--no_logger':
        noLogger = True
    else:
        print('Usage: python3 initializer.py -d to test demo run')
        print('Usage: sudo python3 initializer.py for setting up this service and commiting system autonomy ')
        print('-d  --demo  enable demo mode')
        print('-h  --help  display this message')

if not os.geteuid() == 0 and not demomode:
    sys.exit("\nOnly root can run this script\n")

# This file will:
# Read the config file, then re-configure feeder status file with appropriate fields
# Clear and set crontab jobs (services) to run the serialLogger
# Set crontab jobs to run the controller and ACTIVATOR

#assuming local files are accurate, not pulling from web, but can add in future

# Originally going to write this in Bash but I do not hate myself so switching to python.
# start this service, only works if manually starting as the service will be running if started by the same service
#os.system("systemctl is-active --quiet initializer  || cp '/home/pi/initializer.service' '/etc/systemd/system/initializer.service' && systemctl start initializer && systemctl enable initializer")

if not os.system("systemctl is-active --quiet initializer") == 0 and not demomode:
    # service not running, creating one
    os.system("systemctl status initializer > /home/pi/rawdata/logs/initializer_error_log_"+datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')+".log")
    
    # os.system("cp '/home/pi/initializer.service' '/etc/systemd/system/initializer.service'")
    with open('/etc/systemd/system/initializer.service','w') as f:
        f.write('[Unit]\n')
        f.write('Description=service for initilizer\n')
        f.write('[Service]\n')
        # do not restart and stuff, leave the error log there
        f.write('Type=simple\n')
        f.write('Restart=always\n')
        f.write('RestartSec=1\n')
        if noLogger:
            f.write('ExecStart=python3 /home/pi/initializer.py -nl> /home/pi/rawdata/logs/initializer_output/Current_Instance.log\n')
        else:
            f.write('ExecStart=python3 /home/pi/initializer.py > /home/pi/rawdata/logs/initializer_output/Current_Instance.log\n')
        f.write('[Install]\n')
        f.write('WantedBy=multi-user.target\n')
    os.system("systemctl daemon-reload")
    os.system("systemctl start initializer && systemctl enable initializer")
    exit()

now = datetime.datetime.now()
startTime = time.time()
print ('Started house keeping! Now is '+ now.strftime('%Y-%m-%d %H:%M:%S'))
#adapterName = '/dev/ttyUSB0'


    
if demomode or noLogger:
    os.system('python3 /home/pi/serialLogger.py -d')

def ip4_addresses():
    ip_list = []
    for interface in interfaces():
        for link in ifaddresses(interface)[AF_INET]:
            ip_list.append(link['addr'])
    return ip_list

def writeLoggerService(siteName,adapterName):
    with open('/etc/systemd/system/'+siteName+'.service','w') as f:
        f.write('[Unit]\n')
        f.write('Description=Service for '+siteName+'\n')
        f.write('[Service]\n')
        # do not restart and stuff, leave the error log there
        f.write('Type=simple\n')
        f.write('ExecStart=python3 /home/pi/serialLogger.py '+adapterName+'\n')
        f.write('[Install]\n')
        f.write('WantedBy=multi-user.target\n')
        
def deepRename(oldFileName,newFileName,correctPin):
    with open(oldFileName) as f:
        for line in f:
            if not line.startswith('#'):
                pinStatus = line.strip().split(",")
                break
    os.remove(oldFileName)
    pinStatus[2] = str(correctPin)
    with open(newFileName,'w') as f:
        f.write(','.join(pinStatus)+"\n")
        
# Zero out config cache for new setup
os.system("cp /dev/null '/home/pi/rawdata/current_config.ini'")
    
counter = 0
while True:
    
    # ----------------------------------------------------
    # set up the system according to config file

    config_object = ConfigParser()
    config_object.read("/home/pi/shared_data/config.ini")
    current_config = ConfigParser()
    current_config.read("/home/pi/rawdata/current_config.ini")
    
    activePins = []
    for site in config_object.sections():
        # get pins first
        newFeeder = {}
        feederNum = int(config_object.get(site,'FEEDER_NUMBER'))
        options = config_object.options(site)
        ct = 0;
        for pin in options:
            if pin.startswith('f') and pin.endswith('_pin') and (ct < feederNum or feederNum == 0):
                feederName = pin.rpartition("_pin")[0].upper()
                pinNum = config_object.get(site,pin)
                if (not pinNum in activePins) and (-1 < int(pinNum) <28):
                    newFeeder[feederName] = config_object.get(site,pin)
                    ct = ct +1
                    activePins.append(pinNum)
        
        
        
        site = config_object[site]
        if not site['IP'] in ip4_addresses():
            # not for this machine, skipping
            continue
        siteName = site['SITE_CODE']+"_serialLogger"
        if not demomode and not noLogger and not os.system("systemctl is-active --quiet "+siteName) == 0:
            # The logger for this site is not already running.
            # Need to reconfigure and start the serial looger service
            # Log the error entry, if any
            os.system("systemctl status "+siteName+" > /home/pi/rawdata/logs/"+siteName+"_error_log_"+datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')+".log")
            writeLoggerService(siteName,site['SerialAdapterAddress'])
            os.system("systemctl daemon-reload")
            os.system("systemctl start "+siteName+" && systemctl enable "+siteName)
        
        
            
            
            
        # now we had dealt with the serial logger, we just need to make sure the feeders are right.
        
        
        
        
        # read feeder status
        feederStatus = []
        with open(feederStatusFileName,'r') as f:
            for line in f:
                if not line.startswith('#'):
                    feederStatus.append(line.strip())
        newFeederStatus = []
        for line in feederStatus:
            fs  = line.split(",")
            if fs[0] == site['SITE_CODE']:
                if fs[1] in newFeeder:
                    
                    if fs[2] == newFeeder[fs[1]]:
                        # This means the pin name is consist. writing the line back
                        newFeederStatus.append(line)
                        # Create the file if it does not exist
                        if not os.path.exists(pinTODOFolderName + '/PIN' + fs[2]+'.todo'):
                            if not os.path.exists(pinTODOFolderName+'/PIN' + fs[2]+'.temp'):
                                open(pinTODOFolderName + '/PIN' + fs[2]+'.todo', 'x')
                            else:
                                # yeah, a spot
                                deepRename(pinTODOFolderName+'/PIN' + fs[2]+'.temp', pinTODOFolderName + '/PIN' + fs[2]+'.todo',fs[2])
                    else:
                        # This means the pin position have changed. Modify accordingly.
                        # If the previous file is there, rename it to the new one
                        newPinNum = newFeeder[fs[1]]
                        oldFileName = pinTODOFolderName + '/PIN' + fs[2]+'.todo'
                        newFileName = pinTODOFolderName + '/PIN' + newPinNum+'.todo'
                        
                        badIndicator = False
                        
                        if os.path.exists(oldFileName):
                            # There was a file at the old location
                            if not os.path.exists(pinTODOFolderName+'/PIN' + fs[2]+'.temp'):
                                # If I was not deleted to move spot,
                                if not os.path.exists(newFileName):
                                    # Ideal situation
                                    deepRename(oldFileName, newFileName,newPinNum)
                                else:
                                    # both file exist, bad.
                                    badIndicator = True
                                    os.rename(newFileName,pinTODOFolderName+'/PIN' + newPinNum+'.temp')
                                    # Crysis averted! (not really)
                                    deepRename(oldFileName, newFileName,newPinNum)
                            else:
                                # If I was relocated to temp file,
                                if not os.path.exists(newFileName):
                                    # yes
                                    deepRename(pinTODOFolderName+'/PIN' + fs[2]+'.temp', newFileName,newPinNum)
                                else:
                                    # both file exist, dopuble bad.
                                    badIndicator = True
                                    os.rename(newFileName,pinTODOFolderName+'/PIN' + newPinNum+'.temp')
                                    # Crysis averted?
                                    deepRename(pinTODOFolderName+'/PIN' + fs[2]+'.temp', newFileName,newPinNum)
                        else:
                            # There was no old file (potentially renamed to temp?)
                                
                            if not os.path.exists(newFileName):
                                # Ideal situation
                                if os.path.exists(pinTODOFolderName+'/PIN' + fs[2]+'.temp'):
                                    # there was an old temp file.
                                    # yeah, a spot
                                    deepRename(pinTODOFolderName+'/PIN' + fs[2]+'.temp', newFileName,newPinNum)
                                else:
                                    # just create a new File at location
                                    open(newFileName, 'x')
                            else:
                                # someone taken our spot, bad.
                                badIndicator = True
                                os.rename(newFileName,pinTODOFolderName+'/PIN' + newPinNum+'.temp')
                                # Crysis averted! (again)
                                if os.path.exists(pinTODOFolderName+'/PIN' + fs[2]+'.temp'):
                                    # I was reallocated, thus going into the new spot
                                    deepRename(pinTODOFolderName+'/PIN' + fs[2]+'.temp', newFileName,newPinNum)
                                else:
                                    open(newFileName, 'x')
                        # at this point, other than the possible temp files, the pin is at new location.   
                        # add it back to the new feeder status
                        fs[2] = newFeeder[fs[1]]
                        newFeederStatus.append(','.join(fs))
                        
                        
                    # if the feeder is present, remove it from new feeder dictionary 
                    newFeeder.pop(fs[1])    
                else:
                    # This feeder had been removed, remove it from feeder status and it's PIN file if exist
                    if os.path.exists(pinTODOFolderName + '/PIN' + fs[2]+'.todo'):
                        os.remove(pinTODOFolderName + '/PIN' + fs[2]+'.todo')
            else:
                # This is for another site, skipping
                newFeederStatus.append(line)
                
        # add the feeder that was not present before
        for feederName,pin in newFeeder.items():
            # This means new feeder is connected.
            newFeederStatus.append(site['SITE_CODE']+','+feederName+','+str(pin)+',WAITING')
            # reset the pin file if any was present
            if os.path.exists(pinTODOFolderName+'/PIN' + str(pin) +'.temp'):
                os.remove(pinTODOFolderName+'/PIN' + str(pin) +'.temp')
            # empty the file
            open(pinTODOFolderName + '/PIN' + str(pin) +'.todo', 'w')
        # write it back to feeder status
        with open(feederStatusFileName,'w') as f:
            for fs in newFeederStatus:
                f.write(fs+"\n")
    
    
    # Now delete the sections that was removed from the current config
    for section in current_config.sections():
        if section not in config_object.sections():
            # Disabling the logger service
            siteName = current_config[section]['SITE_CODE']+"_serialLogger"
            os.system("systemctl stop "+siteName+" && systemctl disable "+siteName)
            os.system('sudo rm /etc/systemd/system/'+siteName+'.service')
            
            # Remove PIN files
            options = current_config.options(section)
            for pin in options:
                if pin.startswith('f') and pin.endswith('_pin') :
                    pinNum = current_config.get(section,pin)
                    if not pinNum in activePins:
                        os.system('rm ' +pinTODOFolderName + '/PIN' + pinNum+'.todo')
                        
    
    # Only copy the config file if it is changed 
    if not filecmp.cmp("/home/pi/shared_data/config.ini", "/home/pi/rawdata/current_config.ini")  :
        #  As config is changed, copy the config to current config
        os.system("cp '/home/pi/shared_data/config.ini' '/home/pi/rawdata/current_config.ini'")
        
    #----------------------------------------------------------
    # Done with the config
    # running task
    if not demomode:
        os.system('python3 /home/pi/controller.py &')
        time.sleep(executionDelay)
        os.system('python3 /home/pi/ACTIVATOR.py &')
        time.sleep(endDelay)
    else:
        os.system('python3 /home/pi/controller.py')
        os.system('python3 /home/pi/ACTIVATOR.py')
        
        
    if counter == 0:
        print ('As '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' , execution success!')
        print ('Expect next report in around 10 min')
        counter = counter + 1
    else:
        counter = counter + 1
        if counter == 600:
            counter = 0
    
    
    
    # restarting itself everyday or if it had been two days since last 24 hour
    if time.time() - startTime > 7200 and datetime.datetime.now().hour == restartHour or time.time() - startTime > 172800:
        os.system("journalctl -u initializer.service -p 0..7 --since=-24h10min -x> /home/pi/rawdata/logs/normal_logs/initializer_log_"+datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')+".log")
        os.system('systemctl restart initializer')
        exit()
    
        
    if demomode:
        print('Demo complete! exiting!')
        exit()
        
        
