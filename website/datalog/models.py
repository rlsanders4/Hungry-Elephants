from django.db import models
# Create your models here.

class RFID_tag_number(models.Model):
    
    name = models.CharField(max_length=)

    
class Unix_time(models.Model):
   
    name = models.CharField(max_length=10)

class Site_code(models.Model):
   
    name = models.CharField(max_length=3)



class Anatenna_number(models.Model):
   
    name = models.CharField(max_length=2)
    
