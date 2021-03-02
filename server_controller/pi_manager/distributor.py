#
# Distributor Class.
# Gets formatted schedules from the schedule builder and distributes them to each raspberry pi.
#

from schedules.schedule_builder import ScheduleBuilder
from adminops.models import Pi

class Distributor():
    # pis = List of Pi objects
    def __init__(this, pis):
        this.pis = pis
        for pi in this.pis:
            if pi.connected == False:
                print("(WARN) Pi named " + pi.name + " is not connected.")

    def link_schedule_builder(this, builder):
        this.schedule_builder = builder
        assert(this.schedule_builder is ScheduleBuilder), "no schedule builder found"