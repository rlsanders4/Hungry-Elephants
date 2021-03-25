from django.db import models
from adminops.models import Feeder


class FeedingData(models.Model):
    rfid_tag_number = models.CharField(max_length=50)
    unix_time = models.CharField(max_length=10)
    site_code = models.CharField(max_length=3)
    feeder = models.ForeignKey(Feeder, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.rfid_tag_number+" "+self.unix_time

    
