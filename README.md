# Hungry-Elephants

### Current Python Version: 3.8.5

Docker:
---------------------------------

Quickstart:

1.Have a docker-capable machine, run this command:

docker run -v feeder_data:/code/db -p 8888:8001 -i -t --restart=always --name rfid_feeder demonte77/rfid_feeder:latest

2.Once the server is started, run the following commands to restart it for good luck : )

docker container stop rfid_feeder

docker container start rfid_feeder


3.Then on the same subnet (pi's IP accessable),

Go to https://pi.zopyr.us to download the latest pi image.

Go to https://www.raspberrypi.org/software/ to download the latest Raspberry Pi Imager

4.Click Choose OS, choose the downloaded image.

Plug in a SD card > 8G, choose it as the storage media.

Click "write"

After the process finish, plug the flashed SD card into the prepared PI.


5.If connected though eternet, find what the PI's IP is either plug in a moniter into pi and run "ip address" command (and filter the desired ip address)

Or, go to the router for the network and find connected devices. The pi should be called "RASPBERRYPI"

Or, if wanting to connect to wireless network, plug keyboard and monitor to the pi and manually configure the pi and record the pi address (for later use)


6.If you have a monitor connected, skip to the next step,

Alternatively, connect to the pi VIA RDP is also possible. Write the PI's IP address into the "Remote Desktop Connection" app in windows or "Microsoft remote desktop" app on mac. After connecting, the user name is "pi" and the password is "elephant". (VNC is also available but a monitor need to be pluged for the session to initialize)


7.Now double click the config.ini file on desktop, edit it accoding to instructions. Delete any site you do not want to be there.

8.Now the open the start file on the desktop of pi and click execute in terminal, then click setup regular. The pi will set everything up accordingly.


9.Now your PI setup is complete!


10.Go to the server's IP:8888 (which on local machine it is 127.0.0.1:8888). Go to admin page,

11.Click "Connect a raspberry pi", fill in the info accordingly, the default port for ftp connection to pi is 21, Name can be anything, and the site code is for the antenna box you are going to connect to the pi. (note, you can have multiple virtual PIs with the same IP and port number but different site code and feeders here. This should be similar to the config you wrote in config.ini on pi.

12.You now have to restart the server by: first enter ctrl+c in the terminal window twice to end the tty session, then you have to restart the server (to apply the connection settings by using "docker container stop rfid_feeder" followed by "docker container start rfid_feeder"

12.Add Antennas and Feeders accordingly to the PI you just created.

13.Now go to Home or scheduling to create your schedule! 

14.Active schedules is in...

15.Active schedules page!

16.And obviously the data log page contains all the previous feeding datas that been executed by the Pis.



----------------------------------------------------


To run server in docker:

docker run -v feeder_data:/code/db -p 8888:8001 -i -t --restart=always --name rfid_feeder demonte77/rfid_feeder:latest


To stop the docker:

docker container stop rfid_feeder


To start the docker:

docker container start rfid_feeder


How to update container (keeping the database):

docker container stop rfid_feeder

docker rm rfid_feeder

docker run -v feeder_data:/code/db -p 8888:8001 -i -t --restart=always --name rfid_feeder demonte77/rfid_feeder:latest



How to remove the database:

docker volume rm feeder_data


To create a new custome docker image:

docker build --tag rfid_feeder:latest .




Installing and Running the Server on bare metal:
---------------------------------

1. In the main Hungry-Elephants directory, run `python3 -m venv .venv` (bash) to create a python virtual environment for the project.

2. Still in the main directory, run `source .venv/bin/activate` to activate the python virtual environment.

3. Again in the main directory, run `python3 -m pip install -r requirements.txt` to install dependencies.

4. Change to the /website subfolder and run `python3 manage.py runserver` to run the server.


This server is supposed to write schedule files and send them via ftp to raspberry pis running python scripts. The server is also supposed to read back from the raspberry pis and display the datas in log pages.
