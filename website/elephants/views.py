from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .forms import ScheduleForm, SelectPresetForm
from .models import Schedule, Preset
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect


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
            sched.save()
            print("saved schedule")
            return HttpResponseRedirect(reverse('elephants:index'))
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

def edit_preset_page(request):
    preset = Preset.objects.get(id=request.GET["id"])
    schedules = preset.schedule_set.all()
    context = {'preset': preset, 'schedules':schedules}
    return render (request, 'elephants/edit_preset.html', context)
    #bring up the edit preset page


def index(request):
    context = {'name': 'Hungry Elephants', }
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

def schedule(request):
    context = {'name': 'Schedule', }
    return render(request, 'elephants/schedule.html', context)