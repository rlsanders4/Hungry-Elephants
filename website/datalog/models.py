from django.db import models
from adminops.models import Feeder, Pi
from django.db import transaction
# Create your models here.


class RfidData(models.Model):
    rfid_tag_number = models.CharField(max_length=50)
    unix_time = models.CharField(max_length=10)
    site_code = models.CharField(max_length=3)
    feeder = models.ForeignKey(Feeder, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.rfid_tag_number+" "+self.unix_time

class FeedingData(models.Model):
    #TASK_UUID,EXECUTE_AFTER_UNIX_TIME,TARGET_SITE_CODE,TARGET_FEEDER_NUMBER,AMOUNT(times of feeder activates in one go),
# IF_RECIEVE_FROM_ANTENNA_NUMBER,IF_RECIEVE_FROM_TAG_NUMBER,INTERVAL_TIME,EXPIRE_TIME,REPEAT_X_TIMES
    TASK_UUID = models.CharField(max_length=36)
    EXECUTE_AFTER_UNIX_TIME = models.CharField(max_length=10)
    TARGET_SITE_CODE = models.CharField(max_length=3)
    TARGET_FEEDER_NUMBER = models.CharField(max_length=2)
    AMOUNT = models.CharField(max_length = 1)
    IF_RECIEVE_FROM_ANTENNA_NUMBER = models.CharField(max_length = 2)
    IF_RECIEVE_FROM_TAG_NUMBER = models.CharField(max_length = 16)
    INTERVAL_TIME =models.CharField(max_length = 4)
    EXPIRE_TIME =  models.CharField(max_length = 10)
    REPEAT_X_TIMES = models.CharField(max_length = 1)
    COMPLETED_TIME = models.CharField(max_length = 10)

    
class RFIDLogData(models.Model):
    pi = models.ForeignKey(Pi, on_delete=models.DO_NOTHING, null=True)
    plaintext = models.CharField(max_length=100)
    unix_time = models.CharField(max_length=20)
    site_code = models.CharField(max_length=10)
    antenna_tag = models.CharField(max_length=10)
    rfid = models.CharField(max_length=50)
