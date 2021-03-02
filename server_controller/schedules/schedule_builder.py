#
# Schedule Builder class.
# Accesses the database, grabs active schedules, and formats them for the pi controllers.
#

from pi_manager.distributor import Distributor

class ScheduleBuilder():
    # interval: time interval in ms between schedule pulls
    # distributor: distributor object
    def __init__(this, interval, distributor):
        this.interval = interval
        this.distributor = distributor
        if this.distributor is Distributor:
            try:
                this.distributor.link_schedule_builder(this)
            except AssertionError as e:
                print("ScheduleBuilder: Error linking schedule builder to distributor: " + e)
        # list of strings representing each schedule
        this.schedules = list()

    # start automatically getting schedules on a set interval
    def start(this):
        return 0
    
    def stop(this):
        return 0

    # get schedules on-demand
    def get_schedules(this):
        return 0
