from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# Tentative Pi Connection Model
class Pi(models.Model):
    name = models.CharField(max_length=50, default="Pi") #name seen by users
    ip = models.GenericIPAddressField(protocol='IPv4', null = True, unique=True) #IPv4 address
    port = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(65535)]) #port number
    connected = models.BooleanField(default=False)
    # ASK FOR SITE CODE
    site_code = models.CharField(max_length=10, null=True, unique=True) #site code associated with reader box and antennas

    def __str__(self):
        return self.name + " " + str(self.id)
# Feeder Model
class Feeder(models.Model):
    name = models.CharField(max_length=50, default="Feeder") #name seen by users
    tag = models.CharField(max_length=10) #feeder tag
    connected_to = models.ForeignKey(Pi, on_delete=models.CASCADE) #pi connection

    def __str__(self):
        return self.name

# Antenna Model
class Antenna(models.Model):
    name = models.CharField(max_length=50, default="Antenna") #name seen by users
    tag = models.CharField(max_length=10) #antenna tag
    connected_to = models.ForeignKey(Pi, on_delete=models.CASCADE) #pi connection

    def __str__(self):
        return self.name
