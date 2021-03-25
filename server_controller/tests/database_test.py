import unittest

from django_test_setup import initDjangoTest
initDjangoTest()

from pi_manager.connector import Connector, DummyConnector

from django.contrib.auth.models import User
from adminops.models import Pi, Antenna, Feeder
from elephants.models import Schedule, Elephant

class TestDatabase(unittest.TestCase):

    def setUp(this):
        User.objects.all().delete()
        Pi.objects.all().delete()
        Schedule.objects.all().delete()
        Elephant.objects.all().delete()
        Feeder.objects.all().delete()
        Antenna.objects.all().delete()

    def tearDown(this):
        User.objects.all().delete()
        Pi.objects.all().delete()
        Schedule.objects.all().delete()
        Elephant.objects.all().delete()
        Feeder.objects.all().delete()
        Antenna.objects.all().delete()

    def test_django_setup(this):
        this.assertEqual(list(User.objects.all()), list())
        this.assertEqual(list(Pi.objects.all()), list())
        this.assertEqual(list(Schedule.objects.all()), list())
        this.assertEqual(list(Elephant.objects.all()), list())

    def test_db_add_pi(this):
        this.assertEqual(list(Pi.objects.all()), list())
        pi = Pi()
        pi.name = "TEST PI"
        pi.ip = "192.168.0.4"
        pi.port = 21
        pi.path = "dir"
        pi.site_code = "AAA"
        pi.save()
        this.assertEqual(Pi.objects.get(id=pi.id), pi)

    def test_db_remove_pi(this):
        this.assertEqual(list(Pi.objects.all()), list())
        pi = Pi()
        pi.name = "TEST PI"
        pi.ip = "192.168.0.4"
        pi.port = 21
        pi.path = "dir"
        pi.site_code = "AAA"
        pi.save()
        this.assertEqual(Pi.objects.get(id=pi.id), pi)
        pi.delete()
        this.assertEqual(list(Pi.objects.all()), list())

if __name__ == '__main__':
    unittest.main()