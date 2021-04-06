from django.core.exceptions import ValidationError
from django.db.models.fields import IPAddressField, CharField
from django.forms import ModelForm, Field
from adminops.models import *

class PiForm(ModelForm):
    class Meta:
        model = Pi
        fields = ['name','ip', 'port', 'site_code']

class FeederForm(ModelForm):
    class Meta:
        model = Feeder
        fields = ['name','tag']

class AntennaForm(ModelForm):
    class Meta:
        model = Antenna
        fields = ['name','tag']

