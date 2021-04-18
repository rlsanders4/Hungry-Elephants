from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from elephants.forms import ScheduleForm, PresetForm
from elephants.models import Schedule, Preset, Elephant, PresetSchedule
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from .view import *
import pytz
from django.contrib import messages


est = pytz.timezone("US/Eastern")
central = pytz.timezone("America/Chicago")
'''this method should take schedules (from a preset) and update the date to
the current date and mark all of them as active'''
def create_active_preset_schedules(schedules):
    if(schedules):
        for s in schedules:
            print("original start time: "+str(s.start_time))
            print("original end time: "+str(s.end_time))
            new_start_time = (s.start_date_time.astimezone(central).time().strftime('%H:%M:%S'))
            new_end_time = s.end_date_time.astimezone(central).time().strftime('%H:%M:%S')
            print("new start time: "+new_start_time)
            print("new end time: "+str(new_end_time))
            currentDate = datetime.now(est).strftime('%Y-%m-%d')
            fullTime = currentDate+" "+new_start_time
            new_startDT = datetime.strptime(fullTime, "%Y-%m-%d %H:%M:%S")
            fullTime = currentDate+" "+new_end_time
            new_endDT = datetime.strptime(fullTime, "%Y-%m-%d %H:%M:%S")
            s.start_time_date = new_startDT
            s.end_time_date = new_endDT
            s.active = True
            s.save()

    print("preset schdules are updated!")


'''
Returns active schedules from the database
'''
def active_schedules(request):
    schedules = Schedule.objects.filter(active=True).order_by('-start_time')
    context = {'schedules' : schedules}
    return render(request, 'elephants/active_schedules.html', context)

'''
deletes a preset schedule
'''
def delete_preset_schedule(request):
    schedule = Schedule.objects.get(id=request.GET["id"])
    schedule.delete()
    return edit_preset_page2(request, request.GET["presetid"])

'''
deletes a schedule from the active schedule page
'''
def delete_schedule_activeschedulepage(request):
    delete_schedule(request.GET["id"])
    return active_schedules(request)


'''
deletes a schedule
'''
def delete_schedule(id):
    Schedule.objects.get(pk=id).delete()


'''
executes a preset
'''
def execute_preset(request):
    preset = Preset.objects.get(id=request.GET['id'])
    schedules = preset.schedule_set.all()
    create_active_preset_schedules(schedules)
    messages.info(request, "Preset " + str(request.GET['id']) + " is activated")
    return index(request)

'''
marks a schedule as inactive and returns the active schedules page
'''
def mark_inactive_from_active(request):
    mark_inactive(request.GET["id"])
    return active_schedules(request)


'''
just marks a schedule as inactive
'''
def mark_inactive(id):
    schedule = Schedule.objects.get(pk=id)
    schedule.active = False
    schedule.save()