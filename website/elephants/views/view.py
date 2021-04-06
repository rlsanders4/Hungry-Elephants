from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from elephants.forms import ScheduleForm, PresetForm
from elephants.models import Schedule, Preset, Elephant, PresetSchedule
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from .logic import elephantModuleData
from django.contrib import messages



def index(request):
    elephants = Elephant.objects.all()
    elephantInfo = dict()
    for ele in elephants:
        elephantInfo[ele] = elephantModuleData(ele)

    presets = Preset.objects.all()[:3]
    presetColNum = 6/len(presets)


    context = {'name': 'Hungry Elephants', 'elephantInfo': elephantInfo.items(), 'presets': presets, 'presetColNum':presetColNum}
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