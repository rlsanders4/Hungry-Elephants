from django.db import models
from adminops.models import Feeder, Pi


class FeedingData(models.Model):
    rfid_tag_number = models.CharField(max_length=50)
    unix_time = models.CharField(max_length=10)
    site_code = models.CharField(max_length=3)
    feeder = models.ForeignKey(Feeder, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.rfid_tag_number+" "+self.unix_time

class RFIDLogData(models.Model):
    pi = models.ForeignKey(Pi, on_delete=models.DO_NOTHING, null=True)
    plaintext = models.CharField(max_length=100)
    unix_time = models.CharField(max_length=20)
    site_code = models.CharField(max_length=10)
    antenna_tag = models.CharField(max_length=10)
    rfid = models.CharField(max_length=50)
