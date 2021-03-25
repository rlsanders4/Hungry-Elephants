from django.shortcuts import render
from django.http import HttpResponse
from .models import FeedingData
from .models import RfidData
from django.db import transaction
@transaction.non_atomic_requests
# Create your views here.
def feedingdata(request):
    feedingData = FeedingData.objects.all()
    return render(request, 'datalog/feedingdata.html', {'FeedingData':feedingData})
@transaction.non_atomic_requests
def index(request):
    rfidData = RfidData.objects.all()
    return render(request, 'datalog/index.html', {'RfidData':RfidData})

