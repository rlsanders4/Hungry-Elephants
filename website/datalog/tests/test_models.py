from unittest import TestCase
from datalog.models import FeedingData
from adminops.models import Feeder
# Create your tests here.
class DatalogModelTest(TestCase):

    fdId = -1
    def setUp(self):
        fd = FeedingData(rfid_tag_number="0", unix_time = 1, site_code = "B", feeder = Feeder.objects.all()[0])

        fd.save()
        self.fdId = fd.id
    def test_rfid_tag_number_label(self):
        feedingData = FeedingData.objects.get(id=self.fdId)
        field_label = feedingData._meta.get_field('rfid_tag_number').verbose_name
        self.assertEquals(field_label,'rfid tag number')

    def test_unix_time_label(self):
        feedingData = FeedingData.objects.get(id=self.fdId)
        field_label = feedingData._meta.get_field('unix_time').verbose_name
        self.assertEquals(field_label,'unix time')

    def test_site_code_label(self):
        feedingData = FeedingData.objects.get(id=self.fdId)
        field_label = feedingData._meta.get_field('site_code').verbose_name
        self.assertEquals(field_label,'site code')


    def test_rfid_tag_number_max_length(self):
        feedingData = FeedingData.objects.get(id=self.fdId)
        max_length = feedingData._meta.get_field('rfid_tag_number').max_length
        self.assertEquals(max_length,50)

    def cleanUp(self):
        FeedingData.objects.get(pk = self.fdId).delete()
    