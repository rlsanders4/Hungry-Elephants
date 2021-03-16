#
# Schedule Builder class.
# Accesses the database, grabs active schedules, and formats them for the pi controllers.
#

import time
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

    # start automatically getting schedules on a set interval
    def start(this):
        this.getSchedules()
        time.sleep(1)
        this.getSchedules()
        print(this.schedules)
    
    def stop(this):
        return 0

    def getSchedules(this):
        scheduleList = list(Schedule.objects.all())
        if(scheduleList == this.schedules):
            print("they're already the same")
        else:
            print("getting schedules...")
        
        this.schedules = scheduleList



    #optional callback for a schedule update
    def onScheduleUpdated(this):
        return 0