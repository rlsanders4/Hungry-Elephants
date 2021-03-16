from unittest import TestCase
from datalog.models import FeedingData
import pytest
# Create your tests here.
@pytest.mark.django_db(transaction=True)
class DatalogModelTest(TestCase):


    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        FeedingData.objects.create(rfid_tag_number='1612444051', unix_time='AAA',site_code = 'A1', antenna_number = '900_226000923031' )

    def test_rfid_tag_number_label(self):
        feedingData = FeedingData.objects.get(id=1)
        field_label = feedingData._meta.get_field('rfid_tag_number').verbose_name
        self.assertEquals(field_label,'rfid_tag_number')

    def test_unix_time_label(self):
        feedingData = FeedingData.objects.get(id=1)
        field_label = feedingData._meta.get_field('unix_time').verbose_name
        self.assertEquals(field_label,'unix_time')

    def test_site_code_label(self):
        feedingData = FeedingData.objects.get(id=1)
        field_label = feedingData._meta.get_field('site_code').verbose_name
        self.assertEquals(field_label,'site_code')

    def test_antenna_number_label(self):
        feedingData = FeedingData.objects.get(id=1)
        field_label = feedingData._meta.get_field('antenna_number').verbose_name
        self.assertEquals(field_label,'antenna_number')

    def test_rfid_tag_number_max_length(self):
        feedingData = FeedingData.objects.get(id=1)
        max_length = feedingData._meta.get_field('rfid_tag_number').max_length
        self.assertEquals(max_length,10)

    