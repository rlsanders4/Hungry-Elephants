from django.db import models
from adminops.models import Feeder, Pi
from django.db import transaction
# Create your models here.


class FeedingData(models.Model):
    #TASK_UUID,EXECUTE_AFTER_UNIX_TIME,TARGET_SITE_CODE,TARGET_FEEDER_NUMBER,AMOUNT(times of feeder activates in one go),
# IF_RECIEVE_FROM_ANTENNA_NUMBER,IF_RECIEVE_FROM_TAG_NUMBER,INTERVAL_TIME,EXPIRE_TIME,REPEAT_X_TIMES
    task_uuid = models.CharField(max_length=36)
    execute_after_UNIX_time = models.CharField(max_length=10)
    target_site_code = models.CharField(max_length=3)
    target_feeder_number = models.CharField(max_length=2)
    amount = models.CharField(max_length = 1)
    if_recieve_from_antenna_number = models.CharField(max_length = 2)
    if_recieve_from_tag_number = models.CharField(max_length = 16)
    interval_time =models.CharField(max_length = 4)
    expire_time =  models.CharField(max_length = 10)
    repeat_X_times = models.CharField(max_length = 1)
    completed_time = models.CharField(max_length = 10)

    
class RFIDLogData(models.Model):
    pi = models.ForeignKey(Pi, on_delete=models.DO_NOTHING, null=True)
    plaintext = models.CharField(max_length=100)
    unix_time = models.CharField(max_length=20)
    site_code = models.CharField(max_length=10)
    antenna_tag = models.CharField(max_length=10)
    rfid = models.CharField(max_length=50)
