from django.shortcuts import render
from django.http import HttpResponse
from .models import RFID_tag_number,  Unix_time ,Site_code, Antenna_number

# Create your views here.
def index(request):
    
    rfid_tag_number = RFID_tag_number.objects.all()
    
    unix_time = Unix_time.objects.all()
   
    site_code = Site_code.objects.all()
   
    antenna_number = Antenna_number.objects.all()
    
    return render(request, 'datalog/index.html', {'RFID_tag_number':rfid_tag_number, 'Unix_time':unix_time, 'Site_code':site_code, 'Antenna_number':antenna_number, })
