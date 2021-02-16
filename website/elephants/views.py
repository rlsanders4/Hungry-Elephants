from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render


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
