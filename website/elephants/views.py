from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .forms import ScheduleForm
from .models import Schedule, Preset, Elephant
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect


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
            print(type(form.cleaned_data['elephant']))
            print(type(form.cleaned_data['start_time']))
            print(type(form.cleaned_data['end_time']))
            print(type(form.cleaned_data['interval']))
            print(type(form.cleaned_data['max_feeds']))
            print(type(form.cleaned_data['feeder']))
            return HttpResponseRedirect(reverse('elephants:scheduling'))
    else:
        form = ScheduleForm()

    print("in normal scheduling module")
    return render(request, 'elephants/schedule_module.html', {'form':form})

def preset_scheduling(request):
    if request.method=='POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            sched = Schedule()
            sched.elephant = form.cleaned_data['elephant']
            sched.start_time = form.cleaned_data['start_time']
            sched.end_time = form.cleaned_data['end_time']
            sched.interval = form.cleaned_data['interval']
            sched.max_feeds = form.cleaned_data['max_feeds']
            print("preset scheduling about to save")
            print(request.GET["id"])
            sched.save()
            sched.presets.add(Preset.objects.filter(pk=request.GET["id"])[0])
            sched.save()

            return edit_preset_page(request)
    else:
        form = ScheduleForm()

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



def index(request):
    elephants = Elephant.objects.all()
    print(type(elephants))
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