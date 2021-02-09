# For creating test data
import factory
from factory.django import DjangoModelFactory

from .models import Unix_time, Site_code, Anatenna_number, RFID_tag_number


class UnixTimeFactory(DjangoModelFactory):
    class Meta:
        model = Unix_time

    name = factory.Faker('random_int')


class SiteCodeFactory(DjangoModelFactory):
    class Meta:
        model = Site_Code

    name = factory.Faker('random_int')
    


class AnatennaNumberFactory(DjangoModelFactory):
    class Meta:
        model = Anatenna_number

    name = factory.Faker('random_int')


class RFIDTagNumberFactory(DjangoModelFactory):
    class Meta:
        model = RFID_tag_number

    text = factory.Faker('random_int')

t1 = UnixTimeFactory()
t2 = SiteCodeFactory()
t3 = AnatennaNumberFactory()
t4 = RFIDTagNumberFactory()
t1.name
t2.name
t3.name
t4.name
