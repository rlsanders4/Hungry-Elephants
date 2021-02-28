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
from adminops.models import *
from adminops.forms import *
from django.contrib.auth.views import *

@staff_member_required
def index(request):
    pis = Pi.objects.all()
    for pi in pis:
        pi.feeders = Feeder.objects.filter(connected_to=pi.id).count()
        pi.antennas = Antenna.objects.filter(connected_to=pi.id).count()
    return render(request, 'adminops/index.html', {"name": "Hungry Elephants Administration", "pis": pis})

@staff_member_required
def pisetup(request):
    if request.method == "POST":
        form = PiForm(request.POST)
        if form.is_valid():
            pi = Pi()
            pi.name = request.POST["name"]
            pi.ip = request.POST["ip"]
            pi.port = request.POST["port"]
            pi.path = request.POST["path"]
            pi.save()
            return HttpResponseRedirect(reverse('adminops:index'))
    else:
        form = PiForm()
    return render(request, 'adminops/pisetup.html', {"name": "Hungry Elephants Administration", 'form': form})

# editing a pi
@staff_member_required
def piedit(request):
    if request.method == "POST":
        pi = Pi.objects.get(id=request.POST["id"])
        form = PiForm(request.POST)
        if form.is_valid():
            pi.name = request.POST["name"]
            pi.ip = request.POST["ip"]
            pi.port = request.POST["port"]
            pi.path = request.POST["path"]
            pi.save()
            return HttpResponseRedirect(reverse('adminops:index'))
    else:
        pi = Pi.objects.get(id=request.GET["id"])
        feeders = Feeder.objects.filter(connected_to=pi.id)
        antennas = Antenna.objects.filter(connected_to=pi.id)
        form = PiForm(initial={"name": pi.name, "ip": pi.ip, "port": pi.port, "path": pi.path})
        return render(request, 'adminops/piedit.html', {"name": "Hungry Elephants Administration", "pi": pi, "form": form, "feeders": feeders, "antennas": antennas})

# view for returning ONLY the pi list
@staff_member_required
def pilist(request):
    pis = Pi.objects.all()
    for pi in pis:
        pi.feeders = str(len(Feeder.objects.filter(connected_to=pi.id)))
        pi.antennas = str(len(Antenna.objects.filter(connected_to=pi.id)))
    return render(request, 'adminops/pilist.html', {"name": "Hungry Elephants Administration", "pilist": pis})

# view for deleting a pi
@staff_member_required
def pidelete(request):
    pi = Pi.objects.get(id=request.GET["id"])
    pi.delete()
    pis = Pi.objects.all()
    return redirect(reverse('adminops:index'), {"name": "Hungry Elephants Administration", "pilist": pis})

# view for adding a feeder to a pi
@staff_member_required
def feedersetup(request):
    if request.method == "POST":
        form = FeederForm(request.POST)
        if form.is_valid():
            pi = Pi.objects.get(id=request.POST["pid"])
            feeder = Feeder()
            feeder.name = request.POST["name"]
            feeder.tag = request.POST["tag"]
            feeder.connected_to = pi
            feeder.save()
            return redirect("/admin/piedit?id="+str(pi.id))
    else:
        pi = Pi.objects.get(id=request.GET["pid"])
        form = FeederForm(request.POST)
        if "fid" in request.GET:
            feeder = Feeder.objects.get(id=request.GET["fid"])
            form.initial = {"name": feeder.name, "tag": feeder.tag}
            return render(request, 'adminops/feedersetup.html', {"name": "Hungry Elephants Administration", "pi": pi, "feeder": feeder, "form": form})
        else:
            return render(request, 'adminops/feedersetup.html', {"name": "Hungry Elephants Administration", "pi": pi, "form": form})
    

# view for adding an antenna to a pi
@staff_member_required
def antennasetup(request):
    if request.method == "POST":
        form = AntennaForm(request.POST)
        if form.is_valid():
            pi = Pi.objects.get(id=request.POST["pid"])
            antenna = Antenna()
            antenna.name = request.POST["name"]
            antenna.tag = request.POST["tag"]
            antenna.connected_to = pi
            antenna.save()
            return redirect("/admin/piedit?id="+str(pi.id))
    else:
        pi = Pi.objects.get(id=request.GET["pid"])
        form = AntennaForm(request.POST)
        if "fid" in request.GET:
            antenna = Antenna.objects.get(id=request.GET["aid"])
            form.initial = {"name": antenna.name, "tag": antenna.tag}
            return render(request, 'adminops/antennasetup.html', {"name": "Hungry Elephants Administration", "pi": pi, "antenna": antenna, "form": form})
        else:
            return render(request, 'adminops/antennasetup.html', {"name": "Hungry Elephants Administration", "pi": pi, "form": form})

# delete a feeder
@staff_member_required
def feederdelete(request):
    pi = Pi.objects.get(id=request.GET["pid"])
    feeder = Feeder.objects.get(id=request.GET["id"])
    feeder.delete()
    return redirect("/admin/piedit?id="+str(pi.id))

# delete an antenna
@staff_member_required
def antennadelete(request):
    pi = Pi.objects.get(id=request.GET["pid"])
    antenna = Antenna.objects.get(id=request.GET["id"])
    antenna.delete()
    return redirect("/admin/piedit?id="+str(pi.id))

# login view
class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    extra_context = {'next':'/elephants/'}
    
# logout view
class CustomLogoutView(LogoutView):
    template_name = "registration/logout.html"
    next_page = '/accounts/login'

# password reset view
class CustomPasswordResetView(PasswordResetView):
    template_name = "registration/passwordreset.html"
