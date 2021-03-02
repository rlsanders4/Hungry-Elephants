from django.forms import ModelForm
from .models import Schedule, Elephant
from django.db import models
from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from datetime import datetime
from datetime import timedelta



class ScheduleForm(forms.Form):
    elephant = forms.ModelChoiceField(queryset=Elephant.objects.all())
    start_time = forms.DateTimeField(initial=datetime.now())
    end_time = forms.DateTimeField(initial=datetime.now()+timedelta(hours=8))
    interval = forms.DurationField()
    max_feeds = forms.IntegerField()
    default = forms.BooleanField()
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

class SelectPresetForm(forms.Form):
    elephant = forms.ModelChoiceField(queryset=Elephant.objects.all())
    schedule = forms.ModelChoiceField(queryset=Schedule.objects.filter(default=True))

