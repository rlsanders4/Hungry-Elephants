server_controller/README.md
# Hungry-Elephants server_controller

This is the server-side upstream controller program for communicating with Raspberry Pis.  
It is a **separate** process that runs alongside the web server independently of it.  
This program manages Raspberry Pi connections, distribution of feeding schedules, and collection of data logs from the Pis.
As long as the database in the `db` folder exists and has no pending migrations, the server controller will work and can be started and stopped at any time.  
It should, however, be run without interruption, and, if possible, only stopped during downtime of the Hungry Elephants system, such as overnight.

### Configuration

Configuration options for raspberry pis are in `pi_manager/config.py`. Defaults should work correctly with the provided pi images, but they can be changed if needed. Changes to the configuration are not loaded until the controller is restarted.  

Parameters:
* USERNAME - The username used to sign in to the FTP server on each Pi.
* PASSWORD - The password used to sign in to the FTP server on each Pi.
* DATA_DIR - The path to the `server_controller/data` folder
* STATE - the name of the file used to store information about the state of data logs on each Pi.
* SCHEDULES_TEMPLATE_DIR - directory on FTP server with `schedules.todo.template`, should be `shared_data` by default
* LOGDATA_DIR - directory on FTP server with `logdata.csv`, should be `shared_data` by default
* COMPLETED_DIR - directory on FTP server with `completed.todo`, should be `shared_data` by default
* SCHEDULES_TEMPLATE_NAME - file name of schedules template, should be `schedules.todo.template`
* LOGDATA_NAME - file name of logging data, should be `logdata.csv`
* COMPLETED_NAME - file name of completed tasks, should be `completed.todo`
* DUMMY_NUM - used for testing with simulated Pi connections
* DUMMY_STATE - filename of dummy testing state
* DEFAULT_PIN - default pin # for the feeder on a Pi
* DEFAULT_SERIAL - default serial address on each Pi for the antenna box

Configuration of the the django ORM for interfacing with the database is in `django_setup.py`.

### Use

To run the server controller, run main.py with `python3 main.py` from the server_controller folder.  

To gracefully stop the server controller, enter `stop`.

You can pass optional parameters on startup, e.g. `python3 main.py -v -d`:
* `-v` : run in verbose logging mode
* `-s` : suppress all logging
* `-d` : run in dummy mode
* `-c` : cleans the data logging state; starts pulling all logs from the beginning instead of where left off.
* `-ch` : cleans the data logging state and DELETES ALL DATA LOGS in the database before starting logging from the beginning.

`-c` or `-ch` are intended for use when there is an issue with data logging. `-c` will start pulling logs from the beginning, but this can cause duplicates. `-ch` wipes logging and starts over. Only use this if you're okay with losing logs that are in the database but aren't on raspberry pis.

`-d` will simulate a pi connection and pull sample data for testing.

### server_controller folder contents

* `data` - folder containing files transferred between the controller and FTP servers and files tracking the state of data logging
* `data/state` - file storing the state of data logging. List of {pi.id},{line# in logdata.csv},{line# in completed.todo} for each pi. Tracks the last read line number in each log file for each pi.
* `pi_manager` - classes pertaining to connecting to, distributing to, or pulling data from each Pi
* `schedules` - classes for getting schedules and  formatting them and dummy data
* `tests` - unit testing
* `django_setup.py` - django ORM and database config
* `logger.py` - Handles data logging. Can be modified/extended to change logging behavior.
* `main.py` - the main program

### Program operation

The server controller connects the the database using the Django Object Relational Mapping (ORM) via `django_setup.py`. This is how we can use Django models in it.  
The controller creates two threads, a distributor thread and a data puller thread.  
The distributor thread gets the raspberry pi connection info from the database, pulls schedules from the database, then formats them and distributes them as files to each raspberry pi.  
The data puller thread gets raspberry pi connection info and then downloads data logs from each pi over FTP into separately named files for each pi's logs, then inserts those logs into the database.  
The last read log in each file on each pi is tracked.  
Pi connection configs are checked and updated for every iteration of work in each thread.  
By default, the distributor thread waits 2 seconds between iterations, and the data puller waits 10 seconds.