from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .forms import ScheduleForm
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
            sched.save()
            print("saved schedule")
            return HttpResponseRedirect(reverse('elephants:index'))
    else:
        form = ScheduleForm()


    return render(request, 'elephants/schedule_module.html', {'form':form})
