from unittest import TestCase
from adminops.models import Pi
from adminops.models import Feeder
from adminops.models import Antenna



# Create your tests here.
class AdminopsModelTest(TestCase):

    piId = Pi.objects.all()[0].id
    feederId = Feeder.objects.all()[0].id
    antennaId = Antenna.objects.all()[0].id

    #Pi test
    def test_pi_name_label(self):
        name = Pi.objects.get(id=self.piId)
        field_label = name._meta.get_field('name').verbose_name
        self.assertEquals(field_label,'name')

    def test_pi_ip_label(self):
        name = Pi.objects.get(id=self.piId)
        field_label = name._meta.get_field('ip').verbose_name
        self.assertEquals(field_label,'ip')

    def test_pi_port_label(self):
        name = Pi.objects.get(id=self.piId)
        field_label = name._meta.get_field('port').verbose_name
        self.assertEquals(field_label,'port')

    def test_pi_path_label(self):
        name = Pi.objects.get(id=self.piId)
        field_label = name._meta.get_field('path').verbose_name
        self.assertEquals(field_label,'path')

    def test_pi_connected_label(self):
        name = Pi.objects.get(id=self.piId)
        field_label = name._meta.get_field('connected').verbose_name
        self.assertEquals(field_label,'connected')

    def test_pi_site_code_label(self):
        name = Pi.objects.get(id=self.piId)
        field_label = name._meta.get_field('site_code').verbose_name
        self.assertEquals(field_label,'site code')

    #Feeder model
    def test_feeder_name_label(self):
        name = Feeder.objects.get(id=self.feederId)
        field_label = name._meta.get_field('name').verbose_name
        self.assertEquals(field_label,'name')

    def test_feeder_tag_label(self):
        name = Feeder.objects.get(id=self.feederId)
        field_label = name._meta.get_field('tag').verbose_name
        self.assertEquals(field_label,'tag')

    def test_feeder_connected_to_label(self):
        name = Feeder.objects.get(id=self.feederId)
        field_label = name._meta.get_field('connected_to').verbose_name
        self.assertEquals(field_label,'connected to')

    #Antenna Models
    def test_antenna_name_label(self):
        name = Antenna.objects.get(id=self.antennaId)
        field_label = name._meta.get_field('name').verbose_name
        self.assertEquals(field_label,'name')

    def test_antenna_tag_label(self):
        name = Antenna.objects.get(id=self.antennaId)
        field_label = name._meta.get_field('tag').verbose_name
        self.assertEquals(field_label,'tag')

    def test_antenna_connected_to_label(self):
        name = Antenna.objects.get(id=self.antennaId)
        field_label = name._meta.get_field('connected_to').verbose_name
        self.assertEquals(field_label,'connected to')