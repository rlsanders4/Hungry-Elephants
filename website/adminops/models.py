from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# Tentative Pi Connection Model
class Pi(models.Model):
    ip = models.GenericIPAddressField(protocol='IPv4', unique=True) #IPv4 address
    port = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(65535)]) #port number
    #TODO: verification for server paths
    path = models.CharField(max_length=200) #path of file server
    connected = models.BooleanField(default=False)