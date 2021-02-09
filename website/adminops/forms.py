from django.forms import ModelForm
from adminops.models import Pi

class PiForm(ModelForm):
    class Meta:
        model = Pi
        fields = ['ip', 'port', 'path']
