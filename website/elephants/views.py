from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .forms import ScheduleForm, SelectPresetForm
from .models import Schedule
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect



def index(request):
    context = {'name': 'Hungry Elephants', }
    return render(request, 'elephants/index.html', context)

def feeders(request):
    context = {'name': 'Feeders', }
    return render(request, 'elephants/feeders.html', context)

def scheduling(request):
    if request.method=='POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            sched = Schedule()
            sched.elephant = form.cleaned_data['elephant']
            sched.start_time = form.cleaned_data['start_time']
            sched.end_time = form.cleaned_data['end_time']
            sched.interval = form.cleaned_data['interval']
            sched.max_feeds = form.cleaned_data['max_feeds']
            sched.default = form.cleaned_data['default']
            sched.save()
            print("saved schedule")
            return HttpResponseRedirect(reverse('elephants:index'))
    else:
        form = ScheduleForm()


    return render(request, 'elephants/schedule_module.html', {'form':form})

def preset_scheduling(request):
    if request.method=='POST':
        form = SelectPresetForm(request.POST)
        if(form.is_valid()):
            s = Schedule()
            elephant =form.cleaned_data['elephant']
            schedule = form.cleaned_data['schedule']
            s.elephant = elephant
            s.start_time = schedule.start_time
            s.end_time = schedule.end_time
            s.interval = schedule.interval
            s.max_feeds = schedule.max_feeds
            s.name = elephant.name+" "+str(schedule.start_time.date())
            s.default = False
            s.save()
            return default_presets_manager(request)
    else:
        return default_presets_manager(request)

def default_presets_manager(request):
    schedules = Schedule.objects.filter(default=False)
    form = SelectPresetForm()
    context = {'non_defaults': schedules, 'selectpresetform':form}
    return render(request, 'elephants/default_schedule_selection.html', context)

def markpreset(request):
    schedule = Schedule.objects.get(id=request.GET["id"])
    schedule.default=True
    schedule.save()
    return default_presets_manager(request)


