#
# Connector Class
# Gets pi connections from the DB, tests and updates connection status
#

from adminops.models import Pi

class Connector():
    # dummyMode: True iff simulated connections are desired for the sake of testing
    def __init__(this, dummyMode):
        this.dummyMode = dummyMode

    # get pi connections from the DB
    def connect_pis(this):
        if this.pis is None:
            this.pis = list(Pi.objects.all())
        else:
            oldpis = this.pis
            this.pis = list(Pi.objects.all())
            # check if the pis have updated in the DB
            if this.pis != oldpis:
                for pi in this.pis:
                    pi.connected = verify_connection(pi)
                    pi.save()
            # if the pis haven't changed...
            else:
                return 0

    def get_pis(this):
        return this.pis



def verify_connection(pi):
    #TODO
    return False