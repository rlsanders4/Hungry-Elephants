from django.contrib import admin

# Register your models here.
from .models import Elephant, Schedule

admin.site.register(Elephant)
admin.site.register(Schedule)