from unittest import TestCase as unitTC
from django.test import TestCase as  testTC
from http import HTTPStatus
from elephants.forms import ScheduleForm
from elephants.models import Elephant
from adminops.models import Feeder
from django.db import transaction, IntegrityError

# Create your tests here.


'''elephant
start_time
end_time
interval
max_feeds
feeder'''

class UnitTests(unitTC):

    def testeasy(self):
        self.assertTrue(True, True)

class FormTest(unitTC):
    def test_schedule_form(self):
        data = {
            'elephant': Elephant.objects.get(pk=1),
            'start_time': "2021-03-09 18:53:34-06:00",
            'end_time': "2021-03-09 18:53:34-06:00",
            'interval': "0:00:06",
            'max_feeds': 1,
            'feeder': Feeder.objects.get(pk=3),
        }
        form = ScheduleForm(data = data)
        self.assertTrue(form.is_valid())

    def test_schedule_form2(self):
        data = {
            'elephant': Elephant.objects.get(pk=1),
            'start_time': "2021-03-09 18:53:00",
            'end_time': "2021-03-09 18:53:34",
            'interval': "0:00:06",
            'max_feeds': 1,
            'feeder': Feeder.objects.get(pk=3),
        }
        form = ScheduleForm(data=data)
        self.assertTrue(form.is_valid())

    def test_schedule_form3(self):
        data = {
            'elephant': Elephant.objects.get(pk=2),
            'start_time': "2021-03-09 18:53:00",
            'end_time': "2021-03-09 18:53:34",
            'interval': "0:00:06",
            'max_feeds': 1,
            'feeder': Feeder.objects.get(pk=3),
        }
        form = ScheduleForm(data=data)
        self.assertTrue(form.is_valid())



    def test_schedule_form4(self):
        data = {
            'elephant': Elephant.objects.get(pk=2),
            'start_time': "2021-03-09 18:53:00",
            'end_time': "2021-03-10 20:53:34",
            'interval': "0:00:06",
            'max_feeds': 1,
            'feeder': Feeder.objects.get(pk=3),
        }
        form = ScheduleForm(data=data)
        self.assertTrue(form.is_valid())

    def test_schedule_form5(self):
        data = {
            'elephant': Elephant.objects.get(pk=1),
            'start_time': "2021-03-09 18:53:34-06:00",
            'end_time': "2021-03-10 20:53:34",
            'interval': "0:00:06",
            'max_feeds': 1,
            'feeder': Feeder.objects.get(pk=3),
        }
        form = ScheduleForm(data=data)
        self.assertTrue(form.is_valid())

    def test_schedule_form6(self):
        data = {
            'elephant': Elephant.objects.get(pk=1),
            'start_time': "2021-03-09 18:53:34-06:00",
            'end_time': "2021-03-09 18:53:34-06:00",
            'interval': "0:00:06",
            'max_feeds': 1,
            'feeder': Feeder.objects.get(pk=3),
        }
        form = ScheduleForm(data=data)
        self.assertTrue(form.is_valid())


    def test_schedule_form7(self):
        data = {
            'elephant': Elephant.objects.get(pk=1),
            'start_time': "2021-03-09 18:53:34-06:00",
            'end_time': "2021-03-09 18:53:34-06:00",
            'interval': "0:02:00",
            'max_feeds': 1,
            'feeder': Feeder.objects.get(pk=3),
        }
        form = ScheduleForm(data=data)
        self.assertTrue(form.is_valid())

    def test_schedule_form8(self):
        data = {
            'elephant': Elephant.objects.get(pk=1),
            'start_time': "2021-03-09 18:53:34-06:00",
            'end_time': "2021-03-09 18:53:34-06:00",
            'interval': "0:02:00",
            'max_feeds': 10,
            'feeder': Feeder.objects.get(pk=3),
        }
        form = ScheduleForm(data=data)
        self.assertTrue(form.is_valid())


    def test_schedule_form9(self):
        data = {
            'elephant': Elephant.objects.get(pk=1),
            'start_time': "2021-03-09 18:53:34-06:00",
            'end_time': "2021-03-09 18:53:34-06:00",
            'interval': "0:02:00",
            'max_feeds': 500,
            'feeder': Feeder.objects.get(pk=3),
        }
        form = ScheduleForm(data=data)
        self.assertFalse(form.is_valid())


    def test_schedule_form10(self):
        data = {
            'elephant': Elephant.objects.get(pk=1),
            'start_time': "2021-03-09 18:53:34-06:00",
            'end_time': "2021-03-09 18:53:34-06:00",
            'interval': "2",
            'max_feeds': 1,
            'feeder': Feeder.objects.get(pk=3),
        }
        form = ScheduleForm(data=data)
        self.assertTrue(form.is_valid())