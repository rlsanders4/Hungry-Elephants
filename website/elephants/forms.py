from django.forms import ModelForm
from .models import Schedule, Elephant
from .models import Feeder
from django.db import models
from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from datetime import datetime
from datetime import timedelta
 

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('elephant', 'start_time', 'end_time', 'interval', 'max_feeds', 'feeder',)
        widgets = {
            'elephant': forms.Select(attrs={'class': 'form-control col-4'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control col-4'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control col-4'}),
            'interval': forms.TextInput(attrs={'class': 'form-control col-4'}),
            'max_feeds': forms.NumberInput(attrs={'class': 'form-control col-4'}),
<<<<<<< HEAD
            'feeder': forms.Select(attrs={'class': 'form-control col-4'}),
        }
=======
            'feeder': forms.SelectMultiple(attrs={'class': 'form-control col-4'}),
            'presets': forms.Select(attrs={'class': 'form-control col-4'}),
        }

        '''
        ['%Y-%m-%d %H:%M:%S',    # '2006-10-25 14:30:59'
         '%Y-%m-%d %H:%M',       # '2006-10-25 14:30'
         '%Y-%m-%d',             # '2006-10-25'
         '%m/%d/%Y %H:%M:%S',    # '10/25/2006 14:30:59'
         '%m/%d/%Y %H:%M',       # '10/25/2006 14:30'
         '%m/%d/%Y',             # '10/25/2006'
         '%m/%d/%y %H:%M:%S',    # '10/25/06 14:30:59'
         '%m/%d/%y %H:%M',       # '10/25/06 14:30'
         '%m/%d/%y']             # '10/25/06'
        '''
>>>>>>> d81c38ea09bd11b0a02734b20ba5d8634f4e0892
