from django.shortcuts import render
from django.http import HttpResponse
from .models import FeedingData

# Create your views here.
def index(request):
    feedingData = FeedingData.objects.all()
    return render(request, 'datalog/index.html', {'FeedingData':feedingData})
