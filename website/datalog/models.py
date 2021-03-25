from django.db import models
# Create your models here.

class RfidData(models.Model):
    rfid_tag_number = models.CharField(max_length=10)
    unix_time = models.CharField(max_length=10)
    site_code = models.CharField(max_length=3)
    antenna_number = models.CharField(max_length=10)

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
    Unknown = models.CharField(max_length = 10)

    
