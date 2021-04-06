#!/usr/bin/env python3
import PySimpleGUI as sg
import os
sg.theme('Kayak')
#sg.theme('HotDogStand')

layout = [[sg.Text("Control panel for pi",font = ('sans-serif',25),text_color=('dark green') )],
          [sg.Button("setup regular",font = ('sans-serif',15))],
          [sg.Button("setup no logger",font = ('sans-serif',15))],
          [sg.Button("STOP!",button_color=('white', 'red'),font = ('mono',35))],
          [sg.Button("STOP!, but keeping files",button_color=('white', 'orange red'),font = ('mono',18))],
          [sg.Text("Test:",font = ('sans-serif',18),text_color=('dark green'))],
          [sg.Button("test initializer",font = ('sans-serif',15))],
          [sg.Button("test logger",font = ('sans-serif',15))],
          [sg.Button("run controller",font = ('sans-serif',15))],
          [sg.Button("run ACTIVATOR",font = ('sans-serif',15))],
          [sg.Text(" ",font = ('sans-serif',18))],
          [sg.Button("Backup to Image",font = ('sans-serif',15))],
          [sg.Button("exit",font = ('sans-serif',15))]]

# Create the window
window = sg.Window("Control", layout)

# Create an event loop
while True:
    event, values = window.read()
    if event == "setup regular":
        os.system("sudo python3 /home/pi/initializer.py")
    if event == "setup no logger":
        os.system("sudo python3 /home/pi/initializer.py -nl")
    if event == "STOP!":
        os.system("sudo python3 /home/pi/BIG_RED_STOP_BUTTON.py")
    if event == "STOP!, but keeping files":
        os.system("sudo python3 /home/pi/BIG_RED_STOP_BUTTON.py -kf")
    if event == "test initializer":
        os.system("sudo python3 /home/pi/initializer.py -d")
    if event == "test logger":
        os.system("sudo python3 /home/pi/serialLogger.py -d")
    if event == "run controller":
        os.system("sudo python3 /home/pi/controller.py")
    if event == "run ACTIVATOR":
        os.system("sudo python3 /home/pi/ACTIVATOR.py &")
    if event == "Backup to Image":
        os.system("sudo bash /home/pi/createImage.sh")
    # End program if user closes window or
    # presses the exit button
    if event == "exit" or event == sg.WIN_CLOSED:
        break

window.close()