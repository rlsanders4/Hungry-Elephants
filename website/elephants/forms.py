from django.forms import ModelForm
from .models import Schedule, Elephant, PresetSchedule
from .models import Feeder
from django.db import models
from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from datetime import datetime
from datetime import timedelta

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('elephant', 'start_date','start_time', 'end_date', 'end_time', 'interval', 'max_feeds', 'feeder',)
        widgets = {
            'elephant': forms.Select(attrs={'class': 'form-control col-4'}),
            'start_time': forms.TimeInput(attrs={'class':'form-control col-4', 'type' : 'time'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control col-4', 'type' : 'date'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control col-4', 'type' : 'time'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control col-4','type' : 'date'}),
            'interval': forms.TextInput(attrs={'class': 'form-control col-4'}),
            'max_feeds': forms.NumberInput(attrs={'class': 'form-control col-4'}),
            'feeder': forms.Select(attrs={'class': 'form-control col-4'}),
        }

class PresetForm(forms.ModelForm):
    class Meta:
        model = PresetSchedule
        fields = ('elephant', 'start_time', 'end_time', 'interval', 'max_feeds', 'feeder',)
        widgets = {
            'elephant': forms.Select(attrs={'class': 'form-control col-4'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control col-4', 'type' : 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control col-4', 'type' : 'time'}),
            'interval': forms.TextInput(attrs={'class': 'form-control col-4'}),
            'max_feeds': forms.NumberInput(attrs={'class': 'form-control col-4'}),
            'feeder': forms.Select(attrs={'class': 'form-control col-4'}),
        }