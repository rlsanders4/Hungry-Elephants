#!/usr/bin/env python3
import PySimpleGUI as sg
import os
sg.theme('Kayak')
#sg.theme('HotDogStand')

layout = [[sg.Text("Inividual test units",font = ('sans-serif',25),text_color=('dark green') )],
          [sg.Text(" ",font = ('sans-serif',18))],
          [sg.Button("STOP!",button_color=('white', 'red'),font = ('mono',35))],
          [sg.Button("STOP!, but keeping files",button_color=('white', 'orange red'),font = ('mono',18))],
          [sg.Text(" ",font = ('sans-serif',18))],
          [sg.Button("setup initializer",font = ('sans-serif',15))],
          [sg.Button("test initializer",font = ('sans-serif',15))],
          [sg.Button("review initializer",font = ('sans-serif',15))],
          [sg.Text(" ",font = ('sans-serif',18))],
          [sg.Button("setup logger",font = ('sans-serif',15))],
          [sg.Button("test logger",font = ('sans-serif',15))],
          [sg.Button("review logger",font = ('sans-serif',15))],
          [sg.Text(" ",font = ('sans-serif',18))],
          [sg.Button("setup controller",font = ('sans-serif',15))],
          [sg.Button("test controller",font = ('sans-serif',15))],
          [sg.Button("review controller",font = ('sans-serif',15))],
          [sg.Text(" ",font = ('sans-serif',18))],
          [sg.Button("setup ACTIVATOR",font = ('sans-serif',15))],
          [sg.Button("test ACTIVATOR",font = ('sans-serif',15))],
          [sg.Button("review ACTIVATOR",font = ('sans-serif',15))],
          [sg.Text(" ",font = ('sans-serif',18))],
          [sg.Button("setup no logger",font = ('sans-serif',15))],
          [sg.Button("exit",font = ('sans-serif',15))]]

# Create the window
window = sg.Window("Test", layout)

# Create an event loop
while True:
    event, values = window.read()

    if event == "setup no logger":
        os.system("sudo python3 /home/pi/initializer.py -nl")
    if event == "STOP!":
        os.system("sudo python3 /home/pi/BIG_RED_STOP_BUTTON.py")
    if event == "STOP!, but keeping files":
        os.system("sudo python3 /home/pi/BIG_RED_STOP_BUTTON.py -kf")
        
    if event == "setup initializer":
        os.system("mousepad /home/pi/shared_data/config.ini &")
        os.system("rm -f /home/pi/rawdata/tasks_running/PIN*.todo")
        os.system("cp /home/pi/rawdata/tasks_running/example_files/* /home/pi/rawdata/tasks_running")
        os.system("pcmanfm /home/pi/rawdata/tasks_running")
        os.system("mousepad /home/pi/rawdata/tasks_running/PIN2.todo &")
        os.system("mousepad /home/pi/rawdata/tasks_running/PIN3.todo &")
        os.system("cp /home/pi/shared_data/feeder.status.demo /home/pi/shared_data/feeder.status")
        os.system("mousepad /home/pi/shared_data/feeder.status")
    if event == "test initializer":
        os.system("sudo python3 /home/pi/initializer.py -d")
    if event == "review initializer":
        os.system("mousepad /home/pi/rawdata/tasks_running/PIN2.todo &")
        os.system("mousepad /home/pi/rawdata/tasks_running/PIN3.todo &")
        os.system("mousepad /home/pi/shared_data/feeder.status")
        
    if event == "setup logger":
        os.system("mousepad /home/pi/rawdata/exampledata.csv &")
        os.system("cp /dev/null /home/pi/rawdata/serialdata.csv")
        os.system("mousepad /home/pi/rawdata/serialdata.csv")
        os.system("cp /dev/null /home/pi/shared_data/logdata.csv")
        os.system("mousepad /home/pi/shared_data/logdata.csv")
        os.system("cp /dev/null /home/pi/rawdata/rfidstatus.txt")
        os.system("mousepad /home/pi/rawdata/rfidstatus.txt")
    if event == "test logger":
        os.system("sudo python3 /home/pi/serialLogger.py -d")
    if event == "review logger":
        os.system("mousepad /home/pi/rawdata/serialdata.csv")
        os.system("mousepad /home/pi/shared_data/logdata.csv")
        os.system("mousepad /home/pi/rawdata/rfidstatus.txt")
        
        
    if event == "setup controller":
        os.system("mousepad /home/pi/shared_data/feeder.status &")
        os.system("pcmanfm /home/pi/rawdata/tasks_running")
        os.system("mousepad /home/pi/rawdata/rfidstatus.txt")
        os.system("cp /dev/null /home/pi/shared_data/schedule.todo")
        os.system("mousepad /home/pi/shared_data/schedule.todo")
        os.system("mousepad /home/pi/shared_data/schedule.todo.templet")
        os.system("cp /dev/null /home/pi/shared_data/completed.todo")
        os.system("mousepad /home/pi/shared_data/completed.todo")
    if event == "test controller":
        os.system("sudo python3 /home/pi/controller.py")
    if event == "review controller":
        os.system("mousepad /home/pi/shared_data/feeder.status &")
        os.system("mousepad /home/pi/shared_data/schedule.todo &")
        os.system("mousepad /home/pi/shared_data/schedule.todo.templet &")
        os.system("mousepad /home/pi/shared_data/completed.todo")
        
        
    if event == "setup ACTIVATOR":
        os.system("mousepad /home/pi/shared_data/feeder.status &")
        os.system("pcmanfm /home/pi/rawdata/tasks_running")
        os.system("mousepad /home/pi/rawdata/tasks_running/PIN2.todo &")
        os.system("mousepad /home/pi/rawdata/tasks_running/PIN3.todo &")
    if event == "test ACTIVATOR":
        os.system("sudo python3 /home/pi/ACTIVATOR.py &")
    if event == "review ACTIVATOR":
        os.system("mousepad /home/pi/rawdata/tasks_running/PIN2.todo &")
        os.system("mousepad /home/pi/rawdata/tasks_running/PIN3.todo &")



    # End program if user closes window or
    # presses the exit button
    if event == "exit" or event == sg.WIN_CLOSED:
        break

window.close()