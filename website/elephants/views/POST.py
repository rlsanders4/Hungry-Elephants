from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from elephants.forms import ScheduleForm, PresetForm
from elephants.models import Schedule, Preset, Elephant, PresetSchedule
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from .view import edit_preset_page, edit_preset_page2, index
from django.contrib import messages


'''
This is a method that returns a Schedule form
and handles the form submission as well

if the form is valid, a schedule object will be 
created in the database
'''
def schedule(request):
    model = Schedule
    if request.method=='POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            sched = Schedule()
            sched.elephant = form.cleaned_data['elephant']
            sched.start_time = form.cleaned_data['start_time']
            sched.start_date = form.cleaned_data['start_date']
            sched.start_date_time = datetime.combine(sched.start_date, sched.start_time)
            sched.end_time = form.cleaned_data['end_time']
            sched.end_date = form.cleaned_data['end_date']
            sched.end_date_time = datetime.combine(sched.end_date, sched.end_time)
            sched.interval = 60 * form.cleaned_data['interval']
            sched.max_feeds = form.cleaned_data['max_feeds']
            sched.feeder = form.cleaned_data['feeder']
            sched.save()
            print("saved schedule")
            messages.info(request, "New schedule is activated")
            return index(request)
    else:
        form = ScheduleForm(initial={'start_time':'2021-03-18 17:30', 'end_time': '2021-03-18 18:00'})

    print("in normal scheduling module")
    return render(request, 'elephants/schedule_module.html', {'form':form})

'''
Same as the scheduling method but for preset schedule
'''
def preset_scheduling(request):
    if request.method=='POST':
        form = PresetForm(request.POST)
        if form.is_valid():
            currentDate = datetime.today().strftime('%Y-%m-%d')
            sched = Schedule()
            sched.elephant = form.cleaned_data['elephant']
            sched.start_time = form.cleaned_data['start_time'].strftime('%H:%M:%S')
            sched.start_date = currentDate
            new_st = sched.start_date+" "+sched.start_time
            sched.start_date_time = datetime.strptime(new_st, "%Y-%m-%d %H:%M:%S")

            sched.end_time = form.cleaned_data['end_time'].strftime('%H:%M:%S')
            sched.end_date = currentDate
            new_st = sched.end_date+" "+sched.end_time
            sched.end_date_time = datetime.strptime(new_st, "%Y-%m-%d %H:%M:%S")
            sched.interval = 60 * form.cleaned_data['interval']
            sched.max_feeds = form.cleaned_data['max_feeds']
            sched.feeder = form.cleaned_data['feeder']
            sched.active = False
            print("preset scheduling about to save")
            sched.save()
            sched.presets.add(Preset.objects.filter(pk=request.GET["id"])[0])
            sched.save()

            return edit_preset_page(request)
    else:
        form = PresetForm()

    print("in preset scheduling module")
    return render(request, 'elephants/preset_schedule_module.html', {'presetid':request.GET["id"], 'form':form})


