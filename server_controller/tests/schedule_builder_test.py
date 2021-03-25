import unittest, unittest.mock, io
import datetime

from django_test_setup import initDjangoTest
initDjangoTest()

from schedules.schedule_builder import ScheduleBuilder
from pi_manager.distributor import Distributor
from schedules import dummy_data

from django.contrib.auth.models import User
from adminops.models import Pi, Antenna, Feeder
from elephants.models import Schedule, Elephant

class TestScheduleBuilder(unittest.TestCase):

    def setUp(this):
        User.objects.all().delete()
        Pi.objects.all().delete()
        Schedule.objects.all().delete()
        Elephant.objects.all().delete()
        Feeder.objects.all().delete()
        Antenna.objects.all().delete()
        # setup mock STDOUT
        this.patcher = unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
        this.mock_stdout = this.patcher.start()
        # schedule builder
        this.sb = ScheduleBuilder(unittest.mock.MagicMock())
        # create dummy data
        dummy_data.createDummyData()


    def tearDown(this):
        User.objects.all().delete()
        Pi.objects.all().delete()
        Schedule.objects.all().delete()
        Elephant.objects.all().delete()
        Feeder.objects.all().delete()
        Antenna.objects.all().delete()
        dummy_data.clearDummyData()
        this.patcher.stop()

    def test_get_schedules(this):
        this.assertEqual(Elephant.objects.get(name=dummy_data.ELEPHANT_NAME).name, dummy_data.ELEPHANT_NAME)
        this.assertTrue(len(list(Schedule.objects.all())) > 0)
        schedules = list(Schedule.objects.all())
        this.sb.getSchedules()
        this.assertEqual(schedules, this.sb.schedules)

    def test_format_schedule1(this):
        s = Schedule()
        s.elephant = Elephant.objects.get(name=dummy_data.ELEPHANT_NAME)
        s.start_time = datetime.datetime(2021, 3, 19, 8)
        s.end_time = datetime.datetime(2021, 3, 19, 10)
        s.interval = datetime.timedelta(hours=1)
        s.max_feeds = 1
        s.name = "breakfast"
        schedules = [s]
        # get formatted schedule
        result = this.sb.formatSchedules(schedules).split(',')
        uuid = result[0]
        # get schedule string without UUID
        resultNoUUID = ','.join(result[1:])
        this.assertEqual(resultNoUUID, "1616155200,AAA,F1,1,A1,1234567890,3600,1616162400,1\n")

    def test_format_schedule2(this):
        s = Schedule()
        s.elephant = Elephant.objects.get(name=dummy_data.ELEPHANT_NAME)
        s.start_time = datetime.datetime(2021, 3, 19, 1)
        s.end_time = datetime.datetime(2021, 3, 19, 2)
        s.interval = datetime.timedelta(hours=1)
        s.max_feeds = 1
        s.name = "lunch"
        schedules = [s]
        # get formatted schedule
        result = this.sb.formatSchedules(schedules).split(',')
        uuid = result[0]
        # get schedule string without UUID
        resultNoUUID = ','.join(result[1:])
        this.assertEqual(resultNoUUID, "1616130000,AAA,F1,1,A1,1234567890,3600,1616133600,1\n")

    def test_format_schedule3(this):
        s = Schedule()
        s.elephant = Elephant.objects.get(name=dummy_data.ELEPHANT_NAME)
        s.start_time = datetime.datetime(2021, 3, 19, 6)
        s.end_time = datetime.datetime(2021, 3, 19, 7)
        s.interval = datetime.timedelta(minutes=20)
        s.max_feeds = 2
        s.name = "dinner"
        schedules = [s]
        # get formatted schedule
        result = this.sb.formatSchedules(schedules).split(',')
        uuid = result[0]
        # get schedule string without UUID
        resultNoUUID = ','.join(result[1:])
        this.assertEqual(resultNoUUID, "1616148000,AAA,F1,1,A1,1234567890,1200,1616151600,2\n")

    def test_format_schedule4(this):
        s = Schedule()
        s.elephant = Elephant.objects.get(name=dummy_data.ELEPHANT_NAME)
        s.start_time = datetime.datetime(1970, 1, 1, 12)
        s.end_time = datetime.datetime(1970, 1, 1, 13)
        s.interval = datetime.timedelta(minutes=1000)
        s.max_feeds = 100
        s.name = "dinner"
        schedules = [s]
        # get formatted schedule
        result = this.sb.formatSchedules(schedules).split(',')
        uuid = result[0]
        # get schedule string without UUID
        resultNoUUID = ','.join(result[1:])
        this.assertEqual(resultNoUUID, "61200,AAA,F1,1,A1,1234567890,60000,64800,100\n")

    def test_format_schedule5(this):
        s = Schedule()
        s.elephant = Elephant.objects.get(name=dummy_data.ELEPHANT_NAME)
        s.start_time = datetime.datetime(2100, 1, 1, 12)
        s.end_time = datetime.datetime(2150, 1, 1, 13)
        s.interval = datetime.timedelta(minutes=1000)
        s.max_feeds = 100
        s.name = "dinner"
        schedules = [s]
        # get formatted schedule
        result = this.sb.formatSchedules(schedules).split(',')
        uuid = result[0]
        # get schedule string without UUID
        resultNoUUID = ','.join(result[1:])
        this.assertEqual(resultNoUUID, "4102506000,AAA,F1,1,A1,1234567890,60000,5680346400,100\n")



if __name__ == '__main__':
    unittest.main()