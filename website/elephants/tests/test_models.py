from unittest import TestCase
from elephants.models import Elephant
from elephants.models import Preset
from elephants.models import Schedule
import pytest
# Create your tests here.
@pytest.mark.django_db(transaction=True)
class ElephantsModelTest(TestCase):
<<<<<<< HEAD
    @classmethod
   
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Elephant.objects.create(name ='Bob', rfid = '226000923031' )
        Preset.objects.create(name = 'hello')
        elephant1 = Elephant.objects.get(id=1)
        Schedule.objects.create(elephant = elephant1, start_time = datetime.date(2021, 3, 1), end_time = datetime.date(2021, 3, 1), interval = datetime.timedelta(days=0, hours=2), max_feeds = 1, name = 'hello elephant')
        
        

=======

    elephantId = Elephant.objects.all()[0].id
    presetId = Preset.objects.all()[0].id
    scheduleId = Schedule.objects.all()[0].id
>>>>>>> master

    #elephant test
    def test_elephant_name_label(self):
        name = Elephant.objects.get(id=self.elephantId)
        field_label = name._meta.get_field('name').verbose_name
        self.assertEquals(field_label,'name')

    def test_rfid_label(self):
        rfid = Elephant.objects.get(id=self.elephantId)
        field_label = rfid._meta.get_field('rfid').verbose_name
        self.assertEquals(field_label,'rfid')
    
    def test_elephant_name_max_length(self):
        name = Elephant.objects.get(id=self.elephantId)
        max_length = name._meta.get_field('name').max_length
        self.assertEquals(max_length,40)

    def test_rfid_max_length(self):
        rfid = Elephant.objects.get(id=self.elephantId)
        max_length = rfid._meta.get_field('rfid').max_length
        self.assertEquals(max_length,12)
    
    def test_elephant_str(self):
        elephant = Elephant.objects.get(id=self.elephantId)
        expected_object_name = elephant.name
        self.assertEquals(expected_object_name,str(elephant))

    #preset test
    def test_preset_name_label(self):
        name = Preset.objects.get(id=self.presetId)
        field_label = name._meta.get_field('name').verbose_name
        self.assertEquals(field_label,'name')
    
    def test_preset_name_max_length(self):
        name = Preset.objects.get(id=self.presetId)
        max_length = name._meta.get_field('name').max_length
        self.assertEquals(max_length,14)
    
    def test_preset_str(self):
        preset = Preset.objects.get(id=self.presetId)
        expected_object_name = preset.name
        self.assertEquals(expected_object_name,str(preset))

    #schedule test
    def test_schedule_foreign_key(self):
        testSchedule = Schedule.objects.get(id=self.scheduleId)
        self.assertEqual(testSchedule.elephant.name, "ELE")
        self.assertEqual(testSchedule.elephant.rfid, "123_12345678")

    def test_start_time_label(self):
        start_time = Schedule.objects.get(id=  self.scheduleId)
        field_label = start_time._meta.get_field('start_time').verbose_name
        self.assertEquals(field_label,'start time')

    def test_end_time_label(self):
        end_time = Schedule.objects.get(id=self.scheduleId)
        field_label = end_time._meta.get_field('end_time').verbose_name
        self.assertEquals(field_label,'end time')

    def test_interval_label(self):
        interval = Schedule.objects.get(id=self.scheduleId)
        field_label = interval._meta.get_field('interval').verbose_name
        self.assertEquals(field_label,'interval')


    
    def test_schedule_name_max_length(self):
        name = Schedule.objects.get(id=self.scheduleId)
        max_length = name._meta.get_field('name').max_length
        self.assertEquals(max_length,50)

<<<<<<< HEAD
    def test_schedule_presets(self):
        schedule1 = Schedule.objects.get(id=1)
        presets1 = schedule1.presets.create(name = 'test')
        presets1.save()
        self.assertEqual(schedule1.presets.get(pk = preset1.pk), presets1)
        self.assertEqual(presets1.name, "test")
    
    def test_schedule_str(self):
        try:

            schedule = Schedule.objects.get(id=1)
            expected_object_name = schedule.name
            self.assertEquals(expected_object_name, str(schedule))
        except IntegrityError:
            pass
   


=======
>>>>>>> master

    
    
   
    