from django.db import models
# Create your models here.

class FeedingData(models.Model):
    
    rfid_tag_number = models.CharField(max_length=10)
    unix_time = models.CharField(max_length=10)
    site_code = models.CharField(max_length=3)
    antenna_number = models.CharField(max_length=2)

    
