#
# Connector Class
# Gets pi connections from the DB, tests and updates connection status
#

from adminops.models import Pi
from ftplib import FTP

class Connector():
    # dummyMode: True iff simulated connections are desired for the sake of testing
    def __init__(this):
        this.pis = list()

    # get pi connections from the DB
    def connect_pis(this):
        if len(this.pis) == 0:
            this.pis = list(Pi.objects.all())
            for pi in this.pis:
                pi.connected = this.verify_connection(pi)
                pi.save()
        else:
            oldpis = this.pis
            this.pis = list(Pi.objects.all())
            # check if the pis have updated in the DB
            if this.pis != oldpis:
                for pi in this.pis:
                    pi.connected = this.verify_connection(pi)
                    pi.save()

    def get_pis(this):
        assert(len(this.pis) > 0), "No pi connections found"
        return this.pis

    def verify_connection(this, pi):
        pi.ftp = None
        try:
            pi.ftp = FTP(str(pi.ip))
            pi.ftp.login("ftpuser", "password")
            pi.ftp.close()
            print("Pi " + pi.name + " connection established")
            return True
        except Exception:
            print("Pi " + pi.name + " unable to connect")
            return False


class DummyConnector(Connector):
    def verify_connection(this, pi):
        return True