from django.forms import ModelForm
from .models import Schedule, Elephant
from .models import Feeder
from django.db import models
from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from datetime import datetime
from datetime import timedelta


class TimeInput(forms.DateTimeInput):
    input_type = 'time'


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
            'feeder': forms.Select(attrs={'class': 'form-control col-4'}),
        }

class PresetForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('elephant', 'start_time', 'end_time', 'interval', 'max_feeds', 'feeder',)
        widgets = {
            'elephant': forms.Select(attrs={'class': 'form-control col-4'}),
            'start_time': TimeInput(attrs={'class': 'form-control col-4'}),
            'end_time': TimeInput(attrs={'class': 'form-control col-4'}),
            'interval': forms.TextInput(attrs={'class': 'form-control col-4'}),
            'max_feeds': forms.NumberInput(attrs={'class': 'form-control col-4'}),
            'feeder': forms.Select(attrs={'class': 'form-control col-4'}),
        }