from django.shortcuts import render
from django.http import HttpResponse
from .models import FeedingData
from .models import RfidData

# Create your views here.
def feedingdata(request):
    feedingData = FeedingData.objects.all()
    return render(request, 'datalog/feedingdata.html', {'FeedingData':feedingData})

def index(request):
    rfidData = RfidData.objects.all()
    return render(request, 'datalog/index.html', {'RfidData':RfidData})

