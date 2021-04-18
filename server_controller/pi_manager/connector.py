#
# Connector Class
# Gets pi connections from the DB, tests and updates connection status
#

from adminops.models import Pi
from ftplib import FTP
from . import config

tag = "(Connector) "

class Connector():
    # dummyMode: True iff simulated connections are desired for the sake of testing
    def __init__(this, logger):
        this.pis = list()
        this.logger = logger

    # get pi connections from the DB
    def connect_pis(this):
        if len(this.pis) == 0:
            this.pis = list(Pi.objects.all())
            for pi in this.pis:
                pi.connected = this.verify_connection(pi)
                if(pi.connected):
                    this.logger.logInfo(tag + "Pi " + pi.name + " connected")
                try:
                    pi.save(update_fields=["connected"])
                except:
                    this.logger.logWarn(tag + "Error updating Pi. Was it deleted?")
        else:
            oldpis = this.pis
            this.pis = list(Pi.objects.all())
            # check if the pis have updated in the DB
            if this.pis != oldpis:
                for pi in this.pis:
                    pi.connected = this.verify_connection(pi)
                    if(pi.connected):
                        this.logger.logInfo(tag + "Pi " + pi.name + " connected")
                    try:
                        pi.save(update_fields=["connected"])
                    except:
                        this.logger.logWarn(tag + "Error updating Pi. Was it deleted?")

    def get_pis(this):
        if(len(this.pis) == 0):
            this.logger.logWarn(tag + "No pi connections found")
        return this.pis

    def dc_pis(this):
        for pi in this.pis:
            pi.connected = False
            try:
                pi.save(update_fields=["connected"])
            except:
                this.logger.logWarn(tag + "Error updating Pi. Was it deleted?")

    def update_connection_status(this):
        for pi in this.pis:
            pi.connected = this.verify_connection(pi)
            try:
                pi.save(update_fields=["connected"])
            except:
                this.logger.logWarn(tag + "Error updating Pi. Was it deleted?")

    def verify_connection(this, pi):
        try:
            ftp = FTP(str(pi.ip))
            ftp.login(config.USERNAME, config.PASSWORD)
            ftp.close()
            return True
        except Exception:
            this.logger.logWarn(tag + "Pi " + pi.name + " unable to connect")
            return False

    @staticmethod
    def update_pi(pi):
        try:
            pi.save(update_fields=["connected"])
            return True
        except:
            return False



class DummyConnector(Connector):
    def verify_connection(this, pi):
        return True