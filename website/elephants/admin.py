from django.contrib import admin

# Register your models here.
from .models import Elephant, Schedule, Preset, PresetSchedule

#this just registers models so they will appear in the admin page
admin.site.register(Elephant)
admin.site.register(Schedule)
admin.site.register(Preset)
admin.site.register(PresetSchedule)
