from django.forms import ModelForm
from adminops.models import *

class PiForm(ModelForm):
    class Meta:
        model = Pi
        fields = ['name','ip', 'port', 'path']

class FeederForm(ModelForm):
    class Meta:
        model = Feeder
        fields = ['name','tag']

class AntennaForm(ModelForm):
    class Meta:
        model = Antenna
        fields = ['name','tag']
