# Views for the admin section of the site.
# Created by Luke Evers

from django.conf.urls import url
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls.conf import path
from adminops.models import Pi
from adminops.forms import PiForm

@staff_member_required
def index(request):
    pis = Pi.objects.all()
    return render(request, 'adminops/index.html', {"name": "Hungry Elephants Administration", "pis": pis})

@staff_member_required
def pisetup(request):
    if request.method == "POST":
        form = PiForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            pi = Pi()
            pi.ip = request.POST["ip"]
            pi.port = request.POST["port"]
            pi.path = request.POST["path"]
            pi.save()
            return HttpResponseRedirect(reverse('adminops:index'))
    else:
        form = PiForm()
    return render(request, 'adminops/pisetup.html', {"name": "Hungry Elephants Administration", 'form': form})

#TODO: finish
@staff_member_required
def piedit(request):
    if request.method == "POST":
        form = PiForm(request.POST)
    return render(request, 'adminops/piedit.html', {"name": "Hungry Elephants Administration", "ip": request.GET['ip']})

# view for returning ONLY the pi list
@staff_member_required
def pilist(request):
    pis = Pi.objects.all()
    return render(request, 'adminops/pilist.html', {"name": "Hungry Elephants Administration", "pilist": pis})

# view for deleting a pi
@staff_member_required
def pidelete(request):
    pi = Pi.objects.get(id=request.GET["id"])
    pi.delete()
    pis = Pi.objects.all()
    return redirect(reverse('adminops:index'), {"name": "Hungry Elephants Administration", "pilist": pis})