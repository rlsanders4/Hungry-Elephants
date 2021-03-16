#
# Distributor Class.
# Gets formatted schedules from the schedule builder and distributes them to each raspberry pi.
#

from adminops.models import Pi

class Distributor():
    # pis = List of Pi objects
    # interval = interval in s for schedule updating/distributing
    def __init__(this, interval, pis):
        this.interval = interval
        this.pis = pis
        for pi in this.pis:
            if pi.connected == False:
                print("(WARN) Pi named " + pi.name + " is not connected.")

    def link_schedule_builder(this, builder):
        this.schedule_builder = builder
        from schedules.schedule_builder import ScheduleBuilder
        assert(this.schedule_builder is ScheduleBuilder), "no schedule builder found"

    def distribute(this):
        #TODO: create separate thread each time schedules are sent out
        return 0