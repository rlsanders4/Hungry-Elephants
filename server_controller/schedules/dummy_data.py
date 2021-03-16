from elephants.models import Elephant, Schedule
import datetime

def createDummyData():
    e = Elephant()
    e.name = "SERVERCONTROLLER_TEST_ELEPHANT"
    e.rfid = "1234567890"
    e.save()

    s1 = Schedule()
    s1.elephant = e
    s1.start_time = datetime.datetime(2021, 3, 19, 8)
    s1.end_time = datetime.datetime(2021, 3, 19, 10)
    s1.interval = datetime.timedelta(hours=1)
    s1.max_feeds = 1
    s1.name = "breakfast"
    s1.save()

    s2 = Schedule()
    s2.elephant = e
    s2.start_time = datetime.datetime(2021, 3, 19, 1)
    s2.end_time = datetime.datetime(2021, 3, 19, 2)
    s2.interval = datetime.timedelta(hours=1)
    s2.max_feeds = 1
    s2.name = "lunch"
    s2.save()

    s3 = Schedule()
    s3.elephant = e
    s3.start_time = datetime.datetime(2021, 3, 19, 6)
    s3.end_time = datetime.datetime(2021, 3, 19, 7)
    s3.interval = datetime.timedelta(minutes=20)
    s3.max_feeds = 2
    s3.name = "dinner"
    s3.save()

    print("Created:")
    print(e.name)
    print(s1.name)
    print(s2.name)
    print(s3.name)

def clearDummyData():
    els = Elephant.objects.filter(name="SERVERCONTROLLER_TEST_ELEPHANT")
    for e in els:
        Schedule.objects.filter(elephant=e).delete()
    els.delete()
    print("Deleted test data")
