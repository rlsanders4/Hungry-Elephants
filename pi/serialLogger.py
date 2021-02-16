#!/usr/bin/env python
import serial
import time
import csv



demomode = True

ser = serial.Serial(
port='/dev/ttyUSB0',
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

try:
    ser.write("DMIF".encode())
    print("Command sent")
except:
    print("ERROR sending DMIF to serial")
    exit()

if demomode:
    with open(demofilename, "r") as f:
            filelines = f.readlines()
    totalLines = len(filelines)
    linecounter = 0
    print('Operating in demo mode!')
    print('Total lines: ',totalLines)

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
            
        print(ser_bytes)
        #ser_bytes = ser.readline().decode("ascii")
        data = ser_bytes.split(",")
        data.insert(0,str(int(time.time())))
        data[18]=str(0)
        # TODO: refine leaving detection mechenism with the data scheme.
        leaving = (len(data) >19)
        if leaving:
            print("Leaving!")
        

        # Writing to local log
        with open(logfilename,"a") as f:
            writer = csv.writer(f,delimiter=",")
            writer.writerow(data)
            
        # Modifing the status file
        if leaving:
            with open(statusfilename, "r") as f:
                lines = f.readlines()
            with open(statusfilename, "w") as f:
                # If the elephant is leaving, do not write this line back
                for line in lines:
                    if line.strip("\n").split(",")[2] != data[3]:
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
