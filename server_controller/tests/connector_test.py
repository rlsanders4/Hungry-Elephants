import unittest, unittest.mock, io

from django_test_setup import initDjangoTest
initDjangoTest()

from pi_manager.connector import Connector, DummyConnector

from django.contrib.auth.models import User
from adminops.models import Pi, Antenna, Feeder
from elephants.models import Schedule, Elephant

def createPiA():
    pi = Pi()
    pi.name = "Pi A"
    pi.ip = "192.168.0.4"
    pi.port = 21
    pi.path = "dir"
    pi.site_code = "AAA"
    return pi

def createPiB():
    pi = Pi()
    pi.name = "Pi B"
    pi.ip = "192.168.0.4"
    pi.port = 21
    pi.path = "dir"
    pi.site_code = "AAA"
    return pi

class TestConnector(unittest.TestCase):

    def setUp(this):
        User.objects.all().delete()
        Pi.objects.all().delete()
        Schedule.objects.all().delete()
        Elephant.objects.all().delete()
        Feeder.objects.all().delete()
        Antenna.objects.all().delete()
        this.c = Connector()
        # setup mock STDOUT
        this.patcher = unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
        this.mock_stdout = this.patcher.start()

    def tearDown(this):
        User.objects.all().delete()
        Pi.objects.all().delete()
        Schedule.objects.all().delete()
        Elephant.objects.all().delete()
        Feeder.objects.all().delete()
        Antenna.objects.all().delete()
        this.patcher.stop()

    def test_dummy_connector(this):
        dc = DummyConnector()
        this.assertTrue(dc.verify_connection(None))

    def test_connector_fails_1pi(this):
        pi = createPiA()
        pi.ip = "invalid"
        pi.save()
        this.c.connect_pis()
        this.assertFalse(this.c.get_pis()[0].connected)
        this.assertEqual(this.mock_stdout.getvalue(), "Pi Pi A unable to connect\n")

    def test_connector_succeeds_1pi(this):
        createPiA().save()
        this.c.connect_pis()
        this.assertTrue(this.c.get_pis()[0].connected)
        this.assertEqual(this.mock_stdout.getvalue(), "Pi Pi A connected\n")

    def test_updates_disconnected_pi(this):
        pi = createPiA()
        pi.ip = "invalid"
        pi.connected = True
        pi.save()
        # use mock verify_connection to simulate a connection
        with unittest.mock.patch("pi_manager.connector.Connector.verify_connection", unittest.mock.MagicMock(return_value=True)):
            this.c.connect_pis()
        this.assertTrue(this.c.get_pis()[0].connected)
        # try to check the connection
        this.c.update_connection_status()
        # expect connection now to fail
        this.assertFalse(this.c.get_pis()[0].connected)
            
        


if __name__ == '__main__':
    unittest.main()