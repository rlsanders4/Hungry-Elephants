#
# Distributor Class.
# Gets formatted schedules from the schedule builder and distributes them to each raspberry pi.
#

from adminops.models import Pi, Feeder
from ftplib import FTP
from . import config

tag = "(Distributor) "

class Distributor():
    # pis = List of Pi objects
    # interval = interval in s for schedule updating/distributing
    def __init__(this, pis, logger):
        this.logger = logger
        this.pis = pis
        this.feeders = list(Feeder.objects.all())
        for pi in this.pis:
            if pi.connected == False:
                this.logger.logWarn(tag + "Pi named " + pi.name + " is not connected to distributor.")

    def link_schedule_builder(this, builder):
        this.schedule_builder = builder
        from schedules.schedule_builder import ScheduleBuilder
        assert(this.schedule_builder is ScheduleBuilder), "no schedule builder found"

    def distribute(this, scheduleData):
        for pi in this.pis:
            this.logger.logInfo(tag + "Distributing to: " + pi.name)
            this.logger.logInfo(tag + "Data: " + scheduleData)
            try:
                ftp = FTP(str(pi.ip))
                ftp.login(config.USERNAME, config.PASSWORD)
                if(config.TEST_PATH != ""):
                    ftp.cwd(config.TEST_PATH)
                ftp.cwd(config.SCHEDULES_TEMPLATE_DIR)
                with open(config.DATA_DIR + config.SCHEDULES_TEMPLATE_NAME, "w") as file:
                    file.write(scheduleData)
                    file.close()
                with open(config.DATA_DIR + config.SCHEDULES_TEMPLATE_NAME, "rb") as file:
                    ftp.storlines("STOR " + config.SCHEDULES_TEMPLATE_NAME, file)
                    file.close()
                ftp.close()
                this.logger.logInfo(tag + "successfully written to pi")
            except Exception as e:
                this.logger.logWarn(tag + str(e))
                this.logger.logWarn(tag + "Error sending schedule to pi " + pi.name)
                pi.connected = False
                pi.save()
    
    def push_configs_if_updated(this):
        oldFeeders = this.feeders
        newFeeders = list(Feeder.objects.all())
        if(oldFeeders != newFeeders):
            this.feeders = newFeeders
            this.push_configs()       

    def push_configs(this):
        this.logger.logInfo(tag + "Pushing configs to all Pis")
        for pi in this.pis:
            this.push_config(pi)

    def push_config(this, pi):
        try:
            ftp = FTP(str(pi.ip))
            ftp.login(config.USERNAME, config.PASSWORD)
            if(config.TEST_PATH != ""):
                ftp.cwd(config.TEST_PATH)
            ftp.cwd(config.CONFIG_DIR)
            # config file string
            feeders = list(Feeder.objects.filter(connected_to=pi))
            configStr = config.DEFAULT_SITE + "\nIP = " + str(pi.ip) + "\nSITE_CODE = " + str(pi.site_code) + "\nSerialAdapterAddress = " + config.DEFAULT_SERIAL + "\n"
            configStr += "FEEDER_NUMBER = " + str(len(feeders)) + "\n"
            for feeder in feeders:
                configStr += feeder.tag + "_PIN = " + str(feeder.pin) + "\n"

            with open(config.DATA_DIR + str(pi.id) + config.CONFIG_NAME, "w") as file:
                file.write(configStr)
                file.close()
            with open(config.DATA_DIR + str(pi.id) + config.CONFIG_NAME, "rb") as file:
                ftp.storlines("STOR " + config.CONFIG_NAME, file)
                file.close()
            ftp.close()
            this.logger.logInfo(tag + "wrote config.ini to pi " + pi.name)
            return True
        except Exception:
            this.logger.logWarn(tag + "Pi " + pi.name + " unable to send config.ini")
            return False


class DummyDistributor(Distributor):
    def distribute(this, scheduleData):
        for pi in this.pis:
            this.logger.logInfo(tag + "Distributing to: " + pi.name)
            this.logger.logInfo(tag + "Data: " + scheduleData)
    def push_configs(this):
        this.logger.logInfo(tag + "Pushing configs to all Pis")
    def push_config(this, pi):
        this.logger.logInfo(tag + "Pushing config to pi " + pi.name)
