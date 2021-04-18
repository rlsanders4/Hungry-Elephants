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
SCHEDULES_TEMPLATE_NAME = "schedule.todo.template"
# path to the RFID logdata, no '/' at the end
LOGDATA_DIR = "shared_data"
# name of the RFID logdata file
LOGDATA_NAME = "logdata.csv"
# path to the completed schedules, no '/' at the end
COMPLETED_DIR = "shared_data"
# name of the completed schedules file
COMPLETED_NAME = "completed.todo"
# path to the config file
CONFIG_DIR = "shared_data"
# name of the config file
CONFIG_NAME = "config.ini"

# number for dummy data files
DUMMY_NUM = 99
# file for dummy state
DUMMY_STATE = "dummy_state"
# path to the directory containing COMPLETED_DIR and LOGDATA_DIR. For the pi images, this isn't needed. leave empty unless testing
TEST_PATH = ""

##
## config.ini defaults
##
# default pin # to configure on each Pi if none set
DEFAULT_PIN = "2"
# default serial adapter address
DEFAULT_SERIAL = "/dev/ttyUSB0"
# default site number
DEFAULT_SITE = "[site1]"

