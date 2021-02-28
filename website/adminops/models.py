from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# Tentative Pi Connection Model
class Pi(models.Model):
    name = models.CharField(max_length=50, default="Pi") #name seen by users
    ip = models.GenericIPAddressField(protocol='IPv4', unique=True) #IPv4 address
    port = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(65535)]) #port number
    #TODO: verification for server paths
    path = models.CharField(max_length=200) #path of file server
    connected = models.BooleanField(default=False)
    # ASK FOR SITE CODE
    site_code = models.CharField(max_length=10, default="AAA") #site code associated with reader box and antennas

# Feeder Model
class Feeder(models.Model):
    name = models.CharField(max_length=50, default="Feeder") #name seen by users
    tag = models.CharField(max_length=10) #feeder tag
    connected_to = models.ForeignKey(Pi, on_delete=models.CASCADE) #pi connection

# Antenna Model
class Antenna(models.Model):
    name = models.CharField(max_length=50, default="Antenna") #name seen by users
    tag = models.CharField(max_length=10) #antenna tag
    connected_to = models.ForeignKey(Pi, on_delete=models.CASCADE) #pi connection
