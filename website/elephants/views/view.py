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


'''
This returns the index page (home page)
'''
def index(request):
    #get elephants from DB
    elephants = Elephant.objects.all()

    #this holds the data for the submodules on the home page
    elephantInfo = dict()
    for ele in elephants:
        #calling elephantModuleData returns the data associated with a given elephant (ele)
        elephantInfo[ele] = elephantModuleData(ele)

    #get 3 presets
    presets = Preset.objects.all()[:3]

    context = {'name': 'Hungry Elephants', 'elephantInfo': elephantInfo.items(), 'presets': presets}
    return render(request, 'elephants/index.html', context)

'''
Returns the feeders page
'''
def feeders(request):
    context = {'name': 'Feeders', }
    return render(request, 'elephants/feeders.html', context)
'''
Returns a test page
'''
def custom(request):
    context = {'name': 'Custom', }
    return render(request, 'elephants/custom.html', context)

'''
return the presets page
'''
def presets(request):
    context = {'name': 'Presets', }
    return render(request, 'elephants/presets.html', context)

'''
Return the page that lets you edit a preset
'''
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