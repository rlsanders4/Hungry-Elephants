from django.contrib import admin
from datalog.models import FeedingData, RFIDLogData

# Register your models here.
admin.site.register(FeedingData)
admin.site.register(RFIDLogData)


