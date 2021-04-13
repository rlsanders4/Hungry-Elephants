from elephants.models import Elephant, Schedule
from adminops.models import Feeder, Pi
import datetime
from pi_manager import config

ELEPHANT_NAME = "SERVERCONTROLLER_TEST_ELEPHANT"

def createDummyData():
    try:
        site_code = "AAA"
        feeder_tag = "F1"
        with open(config.DATA_DIR + str(config.DUMMY_NUM) + config.COMPLETED_NAME, "w") as file:
            file.write("1605f11d-83e0-4f33-8c6f-c126e72196b2,1614260512,"+str(site_code)+","+feeder_tag+",1,A0,123,3600,1614303712,1,1615866055\n")
            file.write("3424c3fc-b638-490c-b92d-e3d3c4b9b2c5,1614200000,"+str(site_code)+","+feeder_tag+",1,A0,0_0,3600,1614243200,1,1615866055\n")
            file.write("7b5f796e-0ab3-4e53-8450-89ac34fe71d8,1614260512,"+str(site_code)+","+feeder_tag+",3,A0,0_0,3600,1614303712,1,1615866055\n")
            file.write("28114381-fcd8-4291-a8b6-d8b9014dab92,1614260512,"+str(site_code)+","+feeder_tag+",4,A0,0_0,3600,1614303712,1,1615866055\n")
    except:
        print("(WARN) Error creating dummy data for completed.todo")
    try:
        with open(config.DATA_DIR + str(config.DUMMY_NUM) + config.LOGDATA_NAME, "w") as file:
            file.write("1615417344,AAA,A3,900_226000923031\n")
            file.write("1615417344,AAA,A2,900_226000923031\n")
            file.write("1615417572,AAA,A3,900_226000923031\n")
            file.write("1615417572,AAA,A2,900_226000923031\n")
            file.write("1615417572,AAA,A2,900_226000923031\n")
            file.write("1615417572,AAA,A1,900_226000923031\n")
            file.write("1615860848,AAA,A3,900_226000923031\n")
            file.write("1615860848,AAA,A2,900_226000923031\n")
            file.write("1615860848,AAA,A3,900_226000923031\n")
            file.write("1615860848,AAA,A4,900_226000923031\n")
    except:
        print("(WARN) Error creating dummy data for logdata.csv")
