#
# Schedule Builder class.
# Accesses the database, grabs active schedules, and formats them for the pi controllers.
#

import time
import uuid
from elephants.models import Schedule
from adminops.models import Pi, Feeder

tag = "(ScheduleBuilder) "

class ScheduleBuilder():
    # interval: time interval in s between schedule pulls
    # distributor: distributor object
    def __init__(this, distributor, logger):
        this.logger = logger
        this.distributor = distributor
        from pi_manager.distributor import Distributor
        if this.distributor is Distributor:
            try:
                this.distributor.link_schedule_builder(this)
            except AssertionError as e:
                this.logger.logWarn(tag + "Error linking schedule builder to distributor: " + e)
        # list of strings representing each schedule
        this.schedules = list("INIT EMPTY")
        # list of UUIDs for each schedule
        this.scheduleUUIDs = dict()

    # get schedules and distribute if necessary
    def run(this):
        oldSchedules = this.schedules
        newSchedules = this.getSchedules()
        if(oldSchedules != newSchedules):
            this.distributor.distribute(this.formatSchedules())
    
    def getSchedules(this):
        scheduleList = list(Schedule.objects.filter(active=True))
        if(scheduleList != this.schedules):
            this.schedules = scheduleList
            for schedule in this.schedules:
                # create new UUID for each schedule
                # TODO: only create new UUID for new/changed schedules
                this.scheduleUUIDs[schedule.id] = uuid.uuid4()
        return this.schedules

    def formatSchedules(this):
        result = ""
        for schedule in this.schedules:
            try:
                rfid = str(schedule.elephant.rfid)
                startTime = str(int(schedule.start_date_time.timestamp()))
                interval = str(schedule.interval.seconds)
                endTime = str(int(schedule.end_date_time.timestamp()))
                maxFeeds = str(schedule.max_feeds)
                feederTag = str(schedule.feeder.tag)
                antennaTag = "A0" # antenna tag 'A0' means any antenna will activate this schedule
                activations = "1" # default activations in one go
            except:
                this.logger.logWarn(tag + "Error getting schedule data")
                next
            # try to get UUID, create if necessary
            try:
                uuid = str(this.scheduleUUIDs[schedule.id])
            except:
                this.scheduleUUIDs[schedule.id] = uuid.uuid()
                uuid = str(this.scheduleUUIDs[schedule.id])
            # try to get site code, default to any if necessary
            try:
                pi = schedule.feeder.connected_to
                site_code = str(pi.site_code)
            except:
                site_code = "ERR"
                this.logger.logWarn(tag + "Error getting site code for feeder " + feederTag)
            line_arr = [uuid, startTime, site_code, feederTag, activations, antennaTag, rfid, interval, endTime, maxFeeds]
            line = ','.join(line_arr)
            result += line + '\n'
        return result
