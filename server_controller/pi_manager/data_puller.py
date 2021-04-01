#
# DataPuller class.
# Pulls data logs from the pi.
# 

from adminops.models import Pi, Feeder, Antenna
from datalog.models import RFIDLogData, FeedingData
from os import path
from ftplib import FTP
from . import config

tag = "(DataPuller) "

class DataPuller():
    def __init__(this, pis, logger):
        this.logger = logger
        this.pis = pis
        this.logDataLine = dict()
        this.completedLine = dict()
        for pi in this.pis:
            if pi.connected == False:
                this.logger.logWarn(tag + "Pi named " + pi.name + " is not connected to data puller.")
            this.logDataLine[pi.id] = 0 # tracks latest index of data in logdata.csv for each pi
            this.completedLine[pi.id] = 0 #tracks latest index of data in completed.todo for each pi
        if path.exists(config.DATA_DIR + config.STATE):
            this.getState()
        else:
            this.updateState()

    def pullCompleted(this):
        for pi in this.pis:
            this.logger.logInfo(tag + "Pulling " + config.COMPLETED_NAME + " from: " + pi.name)
            try:
                ftp = FTP(str(pi.ip))
                ftp.login(config.USERNAME, config.PASSWORD)
                ftp.cwd(str(pi.path))
                ftp.cwd(config.COMPLETED_DIR)
                with open(config.DATA_DIR + str(pi.id) + config.COMPLETED_NAME, 'wb') as local_file:
                    response = ftp.retrbinary('RETR ' + config.COMPLETED_NAME, local_file.write)
                    if not response.startswith('226'): 
                        raise(Exception("Error transferring file " + str(pi.id) + config.COMPLETED_NAME))
                # open completed.todo file, read, and put into DB
                with open(config.DATA_DIR + str(pi.id) + config.COMPLETED_NAME, "r") as file:
                    problem = False
                    for i, line in enumerate(file):
                        # start working only on new data
                        if(i >= this.completedLine[pi.id]):
                            line = line.strip()
                            if len(line) > 0:
                                this.completedLine[pi.id] += 1 # increment the index for the next latest data
                                try:
                                    feedingData = FeedingData()
                                    columns = line.split(',')
                                    # TODO: FIND WHICH COLUMN IS THE TIMESTAMP FOR COMPLETION
                                    feedingData.unix_time = columns[1]
                                    feedingData.site_code = columns[2]
                                    # if(columns[3] != "F0"):
                                    #     feedingData.feeder = Feeder.objects.get(tag=columns[3])
                                    feedingData.rfid_tag_number = columns[6]
                                    feedingData.save()
                                except:
                                    problem = True
                    if problem:
                        this.logger.logWarn(tag + "There was an issue parsing " + str(pi.id) + config.COMPLETED_NAME)
                    file.close()
                ftp.close()
                this.updateState()
                this.logger.logInfo(tag + "successfully pulled " + config.COMPLETED_NAME + " from pi")
            except Exception as e:
                this.logger.logWarn(tag + str(e))
                this.logger.logWarn(tag + "Error pulling data from pi " + pi.name)
                pi.connected = False
                pi.save()

    def pullLogData(this):
        for pi in this.pis:
            this.logger.logInfo(tag + "Pulling " + config.LOGDATA_NAME + " from: " + pi.name)
            try:
                ftp = FTP(str(pi.ip))
                ftp.login(config.USERNAME, config.PASSWORD)
                ftp.cwd(str(pi.path))
                ftp.cwd(config.LOGDATA_DIR)
                with open(config.DATA_DIR + str(pi.id) + config.LOGDATA_NAME, "wb") as local_file:
                    response = ftp.retrbinary('RETR ' + config.LOGDATA_NAME, local_file.write)
                    if not response.startswith('226'): 
                        raise(Exception("Error transferring file " + str(pi.id) + config.LOGDATA_NAME))
                # open logdata file, read, and put into DB
                with open(config.DATA_DIR + str(pi.id) + config.LOGDATA_NAME, "r") as file:
                    problem = False
                    for i, line in enumerate(file):
                        # start working only on new data
                        if(i >= this.logDataLine[pi.id]):
                            line = line.strip()
                            if len(line) > 0:
                                this.logDataLine[pi.id] += 1 # increment the index for the next latest data
                                rfidLog = RFIDLogData()
                                rfidLog.plaintext = line
                                columns = line.split(',')
                                try:
                                    rfidLog.unix_time = columns[0]
                                    rfidLog.site_code = columns[1]
                                    rfidLog.antenna_tag = columns[2]
                                    rfidLog.rfid =  columns[3]
                                    rfidLog.save()
                                except:
                                    problem = True
                    if(problem):
                        this.logger.logWarn(tag + "There was an issue parsing " + str(pi.id) + config.LOGDATA_NAME)
                    file.close()
                ftp.close()
                this.updateState()
                this.logger.logInfo(tag + "successfully pulled " + config.LOGDATA_NAME + " from pi")
            except Exception as e:
                this.logger.logWarn(tag + str(e))
                this.logger.logWarn(tag + "Error pulling data from pi " + pi.name)
                pi.connected = False
                pi.save()

    def clearLogDataFiles(this):
        for pi in this.pis:
            try:
                ftp = FTP(str(pi.ip))
                ftp.login(config.USERNAME, config.PASSWORD)
                ftp.cwd(str(pi.path))
                ftp.cwd(config.LOGDATA_DIR)
                with open(config.DATA_DIR + str(pi.id) + config.LOGDATA_NAME, "w") as local_file:
                    local_file.write("")
                with open(config.DATA_DIR + str(pi.id) + config.LOGDATA_NAME, "rb") as file:
                    ftp.storlines("STOR " + config.LOGDATA_NAME, file)
            except:
                this.logger.logWarn(tag + "Error connecting to pi " + pi.name)
                pi.connected = False
                pi.save()
            this.logDataLine[pi.id] = 0
        this.updateState()

    def clearCompletedFiles(this):
        for pi in this.pis:
            try:
                ftp = FTP(str(pi.ip))
                ftp.login(config.USERNAME, config.PASSWORD)
                ftp.cwd(str(pi.path))
                ftp.cwd(config.COMPLETED_DIR)
                with open(config.DATA_DIR + str(pi.id) + config.COMPLETED_NAME, "w") as local_file:
                    local_file.write("")
                with open(config.DATA_DIR + str(pi.id) + config.COMPLETED_NAME, "rb") as file:
                    ftp.storlines("STOR " + config.COMPLETED_NAME, file)
            except:
                this.logger.logWarn(tag + "Error connecting to pi " + pi.name)
                pi.connected = False
                pi.save()
            this.completedLine[pi.id] = 0
        this.updateState()

    def cleanState(this):
        for pi in this.pis:
            this.logDataLine[pi.id] = 0
            this.completedLine[pi.id] = 0
        this.updateState()

    def updateState(this):
        with open(config.DATA_DIR + config.STATE, "w") as file:
            for pi in this.pis:
                line = ','.join([str(pi.id), str(this.logDataLine[pi.id]), str(this.completedLine[pi.id])]) + "\n"
                file.write(line)
        this.logger.logInfo(tag + "Updated logging state.")

    def getState(this):
        with open(config.DATA_DIR + config.STATE, "r") as file:
            for line in file:
                line = line.strip().split(',')
                piID = int(line[0])
                this.logDataLine[piID] = int(line[1])
                this.completedLine[piID] = int(line[2])
        this.logger.logInfo(tag + "Retreived logging state.")



#
# Dummy data puller. Pulls from special local files instead of remote files on a pi.
#
class DummyDataPuller(DataPuller):
    def __init__(this, pis, logger):
        this.logger = logger
        this.pis = pis
        this.logDataLine = dict()
        this.completedLine = dict()
        for pi in this.pis:
            if pi.connected == False:
                this.logger.logWarn(tag + "Pi named " + pi.name + " is not connected to data puller.")
            this.logDataLine[pi.id] = 0 # tracks latest index of data in logdata.csv for each pi
            this.completedLine[pi.id] = 0 #tracks latest index of data in completed.todo for each pi
        this.logDataLine[config.DUMMY_NUM] = 0
        this.completedLine[config.DUMMY_NUM] = 0
        if path.exists(config.DATA_DIR + config.DUMMY_STATE):
            this.getState()
        else:
            this.updateState()

    def pullCompleted(this):
        this.logger.logInfo(tag + "Pulling dummy data from " + config.DATA_DIR + str(config.DUMMY_NUM) + config.COMPLETED_NAME)
        try:
            # open completed.todo file, read, and put into DB
            with open(config.DATA_DIR + str(config.DUMMY_NUM) + config.COMPLETED_NAME, "r") as file:
                problem = False
                for i, line in enumerate(file):
                    # start working only on new data
                    if(i >= this.completedLine[config.DUMMY_NUM]):
                        line = line.strip()
                        if len(line) > 0:
                            this.completedLine[config.DUMMY_NUM] += 1 # increment the index for the next latest data
                            try:
                                feedingData = FeedingData()
                                columns = line.split(',')
                                # TODO: FIND WHICH COLUMN IS THE TIMESTAMP FOR COMPLETION
                                feedingData.unix_time = columns[1]
                                feedingData.site_code = columns[2]
                                # if(columns[3] != "F0"):
                                #     feedingData.feeder = Feeder.objects.get(tag=columns[3])
                                feedingData.rfid_tag_number = columns[6]
                                feedingData.save()
                            except:
                                problem = True
                if problem:
                    this.logger.logWarn(tag + "There was an issue parsing " + str(config.DUMMY_NUM) + config.COMPLETED_NAME)
                file.close()
            this.updateState()
            this.logger.logInfo(tag + "successfully pulled dummy data from " + config.DATA_DIR + str(config.DUMMY_NUM) + config.COMPLETED_NAME)
        except Exception as e:
            this.logger.logWarn(tag + str(e))
            this.logger.logWarn(tag + "Error pulling data from " + config.DATA_DIR + str(config.DUMMY_NUM) + config.COMPLETED_NAME)
    

    def pullLogData(this):
        this.logger.logInfo(tag + "Pulling dummy data from " + config.DATA_DIR + str(config.DUMMY_NUM) + config.LOGDATA_NAME)
        try:
            # open logdata file, read, and put into DB
            with open(config.DATA_DIR + str(config.DUMMY_NUM) + config.LOGDATA_NAME, "r") as file:
                problem = False
                for i, line in enumerate(file):
                    # start working only on new data
                    if(i >= this.logDataLine[config.DUMMY_NUM]):
                        line = line.strip()
                        if len(line) > 0:
                            this.logDataLine[config.DUMMY_NUM] += 1 # increment the index for the next latest data
                            rfidLog = RFIDLogData()
                            rfidLog.plaintext = line
                            columns = line.split(',')
                            try:
                                rfidLog.unix_time = columns[0]
                                rfidLog.site_code = columns[1]
                                rfidLog.antenna_tag = columns[2]
                                rfidLog.rfid =  columns[3]
                                rfidLog.save()
                            except:
                                problem = True
                if(problem):
                    this.logger.logWarn(tag + "There was an issue parsing " + config.DATA_DIR + str(config.DUMMY_NUM) + config.LOGDATA_NAME)
                file.close()
            this.updateState()
            this.logger.logInfo(tag + "successfully pulled dummy data from " + config.DATA_DIR + str(config.DUMMY_NUM) + config.LOGDATA_NAME)
        except Exception as e:
            this.logger.logWarn(tag + str(e))
            this.logger.logWarn(tag + "Error pulling data from " + config.DATA_DIR + str(config.DUMMY_NUM) + config.LOGDATA_NAME)

    def getState(this):
        with open(config.DATA_DIR + config.DUMMY_STATE, "r") as file:
            for line in file:
                line = line.strip().split(',')
                piID = int(line[0])
                this.logDataLine[piID] = int(line[1])
                this.completedLine[piID] = int(line[2])
        this.logger.logInfo(tag + "Retreived logging state.")

    def updateState(this):
        with open(config.DATA_DIR + config.DUMMY_STATE, "w") as file:
            line = ','.join([str(config.DUMMY_NUM), str(this.logDataLine[config.DUMMY_NUM]), str(this.completedLine[config.DUMMY_NUM])]) + "\n"
            file.write(line)
        this.logger.logInfo(tag + "Updated logging state.")

    def cleanState(this):
        this.logDataLine[config.DUMMY_NUM] = 0
        this.completedLine[config.DUMMY_NUM] = 0
        this.updateState()
 