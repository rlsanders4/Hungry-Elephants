from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from adminops.models import Feeder


'''
This model represents an elephant
'''
class Elephant(models.Model):
    name = models.CharField(max_length=40)
    rfid = models.CharField(max_length=50)

    def __str__(self):
        return self.name

'''
A preset is a group of schedules that can be executed all at once with the server controller
A preset contain:
    name (of the preset)
Note: the Schedule will handle the many-to-many relationship
'''
class Preset(models.Model):
    name = models.CharField(max_length=14)

    def __str__(self):
        return self.name

''' 
The Schedule model class represents the basic building block for automated elephant feeding.
A schedule includes the following:
    Elephant
    Start Time
    start Date
    End Time
    End Date
    Interval Length
    Max # of Feeds
    Feeder (foreign key to a feeder object)
    Preset (links schedules to presets via many to many field)
    activate (or not) so it's a boolean
'''
class Schedule(models.Model):
    elephant = models.ForeignKey(Elephant, on_delete=models.CASCADE)  # reference to existing elephant in DB
    start_date_time = models.DateTimeField()  # start time
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date_time = models.DateTimeField()  # end time (on the same day as start time, usually)
    end_date = models.DateField()
    end_time = models.TimeField()
    interval = models.DurationField()  # minimum waiting time before repeated feeds to elephant
    max_feeds = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])  # max number of times this schedule can allow feeding the elephant
    name = models.CharField(max_length=50, null=True)
    feeder = models.ForeignKey(Feeder, on_delete=models.CASCADE, null=True)
    presets = models.ManyToManyField(Preset)
    active = models.BooleanField(default=True)

    def __str__(self):
        if(self.name):
            return self.name
        return "Schedule: " + str(self.id)

'''
Same as the schedule class but doesn't have start or end date
'''
class PresetSchedule(models.Model):
    elephant = models.ForeignKey(Elephant, on_delete=models.CASCADE)  # reference to existing elephant in DB
    start_time = models.TimeField()  # start time
    end_time = models.TimeField()  # end time (on the same day as start time, usually)
    interval = models.DurationField()  # minimum waiting time before repeated feeds to elephant
    max_feeds = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])  # max number of times this schedule can allow feeding the elephant
    name = models.CharField(max_length=50, null=True)
    feeder = models.ForeignKey(Feeder, on_delete=models.CASCADE, null=True)
    presets = models.ManyToManyField(Preset)
    active = models.BooleanField(default=True)

    def __str__(self):
        if(self.name):
            return self.name
        return "Preset Schedule: " + str(self.id)