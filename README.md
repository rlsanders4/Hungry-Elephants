# Hungry-Elephants

### Current Python Version: 3.8.5

Docker:
---------------------------------

To run server in docker:
docker run -v feeder_data:/code/db -p 8888:8000 -i -t --restart=always --name rfid_feeder demonte77/rfid_feeder:latest

To stop the docker:
docker container stop rfid_feeder

To start the docker:
docker container start rfid_feeder

How to update container (keeping the database):
docker container stop rfid_feeder
docker rm rfid_feeder
docker run -v feeder_data:/code/db -p 8888:8000 -i -t --restart=always --name rfid_feeder demonte77/rfid_feeder:latest


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
