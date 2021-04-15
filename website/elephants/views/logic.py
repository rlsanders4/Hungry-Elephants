from datalog.models import FeedingData
from elephants.models import Schedule
from datetime import datetime

import pytz
import time


est = pytz.timezone("US/Eastern")
utc = pytz.utc
fmt = "%Y-%m-%d %H:%M:%S"


'''
returns data for the home page tiles
'''
def elephantModuleData(elephant):
    erifd = elephant.rfid
    feedingDataQS = FeedingData.objects.filter(rfid_tag_number = erifd).order_by('-unix_time')
    feedingData = list()
    for fd in feedingDataQS:
        if(int(fd.unix_time)>=int(time.time())-84600):
            feedingData.append(fd)

    lastfed = "never"
    numberFeedingsToday =0
    endOfSchedule = "No Active Schedule"

    if(feedingData):
        lastfed = datetime.fromtimestamp(int(feedingData[0].unix_time), est).strftime("%Y-%m-%d %H:%M:%S")
        numberFeedingsToday = len(feedingData)

    activeSchedules =  Schedule.objects.filter(elephant=elephant).filter(active=True).order_by('-start_time')
    if(activeSchedules):
        endOfSchedule = activeSchedules[0].end_time

    return {"lastfed": lastfed, "feedingstoday": numberFeedingsToday, "currentscheduleends": endOfSchedule}
