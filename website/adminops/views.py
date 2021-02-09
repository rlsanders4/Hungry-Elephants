# Views for the admin section of the site.
# Created by Luke Evers

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def index(request):
    return render(request, 'adminops/index.html')