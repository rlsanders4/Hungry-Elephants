#!/usr/bin/env python3
import serial
import time
import csv
import datetime
import sys


# Default values
demomode = False
serialPort = '/dev/ttyUSB0'

if len(sys.argv) > 1:
    # Some arguments had been passed in. We conly interest in the first one.
    if sys.argv[1] == '-d' or sys.argv[1] == '--demo':
        demomode =True
        print('Demoing!')
    elif sys.argv[1][0] == '/' :
        serialPort = sys.argv[1]
    else:
        print('Usage: python serialLogger.py /dev/ttyUSB0')
        print('First argument should be the serial port the pi should listen on!')
        print('Default: continuously listen to serial port defined for elephant arrival and departure information')
        print('-d  --demo  enable demo mode')
        print('-h  --help  display this message')

if not demomode:
    ser = serial.Serial(
    port = serialPort,
    baudrate = 19200,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.SEVENBITS,
    timeout=1
    )
#ser.flushInput()

logfilename = '/home/pi/rawdata/serialdata.csv'
statusfilename = '/home/pi/rawdata/rfidstatus.txt'
serverlogfilename = '/home/pi/shared_data/logdata.csv'
demofilename = '/home/pi/rawdata/exampledata.csv'



if demomode:
    with open(demofilename, "r") as f:
            filelines = f.readlines()
    totalLines = len(filelines)
    linecounter = 0
    print('Operating in demo mode!')
    print('Total lines: ',totalLines)
else:
    try:
        ser.write("DMIF".encode())
        print("Command sent")
    except:
        print("ERROR sending DMIF to serial")
        exit()

while True:
    try:
        if demomode:
            if linecounter < totalLines:
                ser_bytes = filelines[linecounter]
                linecounter = linecounter + 1
            else:
                break
        else:
            ser_bytes = ser.readline()
            #ser_bytes = ser.readline().decode("ascii")
            
        print(ser_bytes)
        
        data = ser_bytes.strip().split(",")
        data[0] = str(int(time.time()))
        if not len(data) == 19:
            print('ERROR! Input data have a wrong length! expecting 19, got '+str(len(data)))
            print('Input data: '+ser_bytes)
            continue
        
        try:
            x = time.strptime(data[4].split('.')[0],'%H:%M:%S')
            elapsedSec = int(datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds())
        except:
            print("ERROR! Input data have an illegal time elapsed field!")
            continue
        leaving = not elapsedSec == 0
        
        if leaving:
            print("Leaving!")
        

        # Writing to local log
        with open(logfilename,"a") as f:
            # note: this data uses the antenna time while the rest of the logs uses local time on pi
            f.write(ser_bytes)
            
        # Modifing the status file
        if leaving:
            with open(statusfilename, "r") as f:
                lines = f.readlines()
            with open(statusfilename, "w") as f:
                # If the elephant is leaving, do not write this line back
                for line in lines:
                    if line.strip("\n").split(",")[2] != data[3]:
                        # print(line.strip("\n").split(",")[2],data[3])
                        f.write(line)
        else:
            # If not leaving, then append the line
            with open(statusfilename, "a") as f:
                f.write(','.join([data[0],data[2],data[3],data[1]]))
                f.write('\n')
        # Wrting to server log
        with open(serverlogfilename,"a") as f:
            writer = csv.writer(f,delimiter=",")
            if not leaving:
                writer.writerow([data[0],data[2],data[3],data[1]])
    except:
        print("Keyboard Interrupt")
        break
