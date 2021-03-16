#
# Distributor Class.
# Gets formatted schedules from the schedule builder and distributes them to each raspberry pi.
#

from adminops.models import Pi
import smbclient
import io
from ftplib import FTP

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

    def distribute(this, scheduleData):
        for pi in this.pis:
            print("Distributing to: ", end='')
            print(pi.name)
            print(scheduleData)
            if(pi.ftp is not None):
                try:
                    pi.ftp = FTP("192.168.0.4")
                    pi.ftp.login("ftpuser", "password")
                    pi.ftp.cwd("dir")
                    # pi.ftp.delete("schedules.todo.template")
                    with open("schedules.todo.template", "w") as file:
                        file.write(scheduleData)
                        file.close()
                    with open("schedules.todo.template", "rb") as file:
                        pi.ftp.storlines("STOR schedules.todo.template", file)
                        file.close()
                    pi.ftp.close()
                    print("successfully written to pi")
                except Exception as e:
                    print(e)
                    print("Error sending schedule to pi " + pi.name)


class DummyDistributor(Distributor):
    def distribute(this, scheduleData):
        for pi in this.pis:
            print("Distributing to: ", end='')
            print(pi.name)
            print(scheduleData)