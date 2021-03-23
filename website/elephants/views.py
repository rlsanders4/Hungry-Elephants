from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .forms import ScheduleForm, PresetForm
from .models import Schedule, Preset, Elephant, PresetSchedule
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime

def schedule(request):
    model = Schedule
    if request.method=='POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            sched = Schedule()
            sched.elephant = form.cleaned_data['elephant']
            sched.start_time = form.cleaned_data['start_time']
            sched.end_time = form.cleaned_data['end_time']
            sched.interval = form.cleaned_data['interval']
            sched.max_feeds = form.cleaned_data['max_feeds']
            sched.feeder = form.cleaned_data['feeder']
            sched.save()
            print("saved schedule")
            return HttpResponseRedirect(reverse('elephants:schedule'))
    else:
        form = ScheduleForm(initial={'start_time':'2021-03-18 17:30', 'end_time': '2021-03-18 18:00'})

    print("in normal scheduling module")
    return render(request, 'elephants/schedule_module.html', {'form':form})

def preset_scheduling(request):
    if request.method=='POST':
        form = PresetForm(request.POST)
        if form.is_valid():
            currentDate = datetime.today().strftime('%Y-%m-%d')
            sched = Schedule()
            sched.elephant = form.cleaned_data['elephant']
            st = form.cleaned_data['start_time'].strftime('%H:%M:%S')
            new_st = currentDate+" "+st
            sched.start_time = datetime.strptime(new_st, "%Y-%m-%d %H:%M:%S")

            et = form.cleaned_data['end_time'].strftime('%H:%M:%S')
            new_et = currentDate+" "+et
            sched.end_time = datetime.strptime(new_et, "%Y-%m-%d %H:%M:%S")
            sched.interval = form.cleaned_data['interval']
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



def edit_preset_page(request):
    preset = Preset.objects.get(id=request.GET["id"])
    schedules = preset.schedule_set.all()
    context = {'preset': preset, 'schedules':schedules}
    return render (request, 'elephants/edit_preset.html', context)
    #bring up the edit preset page

#this is same as edit_preset_page but just takes an extra param, namely the presetid
def edit_preset_page2(request, id):
    preset = Preset.objects.get(id=id)
    schedules = preset.schedule_set.all()
    context = {'preset': preset, 'schedules':schedules}
    return render (request, 'elephants/edit_preset.html', context)
    #bring up the edit preset page


def delete_preset_schedule(request):
    schedule = Schedule.objects.get(id=request.GET["id"])
    schedule.delete()
    return edit_preset_page2(request, request.GET["presetid"])

def delete_schedule_activeschedulepage(request):
    delete_schedule(request.GET["id"])
    return active_schedules(request)

def delete_schedule(id):
    Schedule.objects.get(pk=id).delete()


def execute_preset(request):
    preset = Preset.objects.get(id=request.GET['id'])
    schedules = preset.schedule_set.all()
    create_active_preset_schedules(schedules)
    return index(request)

def mark_inactive_from_active(request):
    mark_inactive(request.GET["id"])
    return active_schedules(request)

def mark_inactive(id):
    schedule = Schedule.objects.get(pk=id)
    schedule.active = False
    schedule.save()

'''this method should take schedules (from a preset) and update the date to
the current date and mark all of them as active'''
def create_active_preset_schedules(schedules):
    if(schedules):
        for s in schedules:
            new_start_time = (s.start_time.time().strftime('%H:%M:%S'))
            new_end_time = s.end_time.time().strftime('%H:%M:%S')
            print(new_start_time)
            print(new_end_time)
            currentDate = datetime.today().strftime('%Y-%m-%d')
            fullTime = currentDate+" "+new_start_time
            new_startDT = datetime.strptime(fullTime, "%Y-%m-%d %H:%M:%S")
            fullTime = currentDate+" "+new_end_time
            new_endDT = datetime.strptime(fullTime, "%Y-%m-%d %H:%M:%S")
            s.start_time = new_startDT
            s.end_time = new_endDT
            s.active = True
            s.save()

    print("preset schdules are updated!")

def active_schedules(request):
    schedules = Schedule.objects.filter(active=True).order_by('-start_time')
    context = {'schedules' : schedules}
    return render(request, 'elephants/active_schedules.html', context)


def index(request):
    elephants = Elephant.objects.all()
    elephants1 = elephants[:3]
    elephants2 = elephants[3:]
    context = {'name': 'Hungry Elephants', 'elephants1': elephants1, 'elephants2':elephants2}
    return render(request, 'elephants/index.html', context)

def feeders(request):
    context = {'name': 'Feeders', }
    return render(request, 'elephants/feeders.html', context)

def custom(request):
    context = {'name': 'Custom', }
    return render(request, 'elephants/custom.html', context)

def presets(request):
    context = {'name': 'Presets', }
    return render(request, 'elephants/presets.html', context)