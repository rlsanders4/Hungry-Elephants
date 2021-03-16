#
# Schedule Builder class.
# Accesses the database, grabs active schedules, and formats them for the pi controllers.
#

import time
import uuid
from elephants.models import Schedule

class ScheduleBuilder():
    # interval: time interval in s between schedule pulls
    # distributor: distributor object
    def __init__(this, interval, distributor):
        this.interval = interval
        this.distributor = distributor
        from pi_manager.distributor import Distributor
        if this.distributor is Distributor:
            try:
                this.distributor.link_schedule_builder(this)
            except AssertionError as e:
                print("ScheduleBuilder: Error linking schedule builder to distributor: " + e)
        # list of strings representing each schedule
        this.schedules = list()

    # get schedules and distribute if necessary
    def run(this):
        this.getSchedules()
        time.sleep(1)
    
    def getSchedules(this):
        scheduleList = list(Schedule.objects.all())
        if(scheduleList != this.schedules):
            this.schedules = scheduleList
            this.distributor.distribute(this.formatSchedules(this.schedules))

    def formatSchedules(this, scheduleList):
        result = ""
        for schedule in scheduleList:
            startTime = str(int(schedule.start_time.timestamp()))
            interval = str(schedule.interval.seconds)
            endTime = str(int(schedule.end_time.timestamp()))
            line = str(uuid.uuid1()) + "," + startTime + "," + "AAA,F1,1,A1," + str(schedule.elephant.rfid) + "," + interval + "," + endTime + "," + str(schedule.max_feeds)
            result += line + '\n'
        return result
