from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Elephant model
class Elephant(models.Model):
    name = models.CharField(max_length=40)
    rfid = models.CharField(max_length=12)

    def __str__(self):
        return self.name


''' 
The Schedule model class represents the basic building block for automated elephant feeding.
A schedule includes the following:
    Elephant
    Start Time
    End Time
    Interval Length
    Max # of Feeds
'''
class Schedule(models.Model):
    elephant = models.ForeignKey(Elephant, on_delete=models.CASCADE)  # reference to existing elephant in DB
    start_time = models.DateTimeField()  # start time
    end_time = models.DateTimeField()  # end time (on the same day as start time, usually)
    interval = models.DurationField()  # minimum waiting time before repeated feeds to elephant
    max_feeds = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])  # max number of times this schedule can allow feeding the elephant
    name = models.CharField(max_length=50, null=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        if(self.name):
            return self.name
        return "Schedule: " + str(self.id)

