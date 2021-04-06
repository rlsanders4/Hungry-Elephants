from pathlib import Path
# FTP username/password
USERNAME = "pi"
PASSWORD = "elephant"
# data folder, including '/' at the end
DATA_DIR = str(Path(__file__).resolve().parent.parent / "data") + "/"
# stores logging state after stopping
STATE = "state"
##
## paths to and names of various files on raspberry pis
## 
## paths are relative to the root directory referenced in pi.path
## e.g. the complete path to the schedule template will be: pi.path + "/" + SCHEDULE_TEMPLATE_PATH + "/" + SCHEDULE_TEMPLATE_NAME
## 
# path to the schedule template, no '/' at the end
SCHEDULES_TEMPLATE_DIR = "shared_data"
# name of schedule template
SCHEDULES_TEMPLATE_NAME = "schedules.todo.template"
# path to the RFID logdata, no '/' at the end
LOGDATA_DIR = "shared_data"
# name of the RFID logdata file
LOGDATA_NAME = "logdata.csv"
# path to the completed schedules, no '/' at the end
COMPLETED_DIR = "shared_data"
# name of the completed schedules file
COMPLETED_NAME = "completed.todo"

# number for dummy data files
DUMMY_NUM = 99
# file for dummy state
DUMMY_STATE = "dummy_state"
