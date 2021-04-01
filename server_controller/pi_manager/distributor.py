#
# Distributor Class.
# Gets formatted schedules from the schedule builder and distributes them to each raspberry pi.
#

from adminops.models import Pi
from ftplib import FTP
from . import config

tag = "(Distributor) "

class Distributor():
    # pis = List of Pi objects
    # interval = interval in s for schedule updating/distributing
    def __init__(this, pis, logger):
        this.logger = logger
        this.pis = pis
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
                ftp.cwd(str(pi.path))
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


class DummyDistributor(Distributor):
    def distribute(this, scheduleData):
        for pi in this.pis:
            this.logger.logInfo(tag + "Distributing to: " + pi.name)
            this.logger.logInfo(tag + "Data: " + scheduleData)