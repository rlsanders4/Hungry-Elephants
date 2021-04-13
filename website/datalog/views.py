from django.shortcuts import render
from django.http import HttpResponse
from .models import FeedingData
from .models import RfidData
import sqlite3
#from django.db import transaction
#@transaction.non_atomic_requests
# Create your views here.
def feedingdata(request):
    feedingData = FeedingData.objects.all()
    return render(request, 'datalog/feedingdata.html', {'FeedingData':feedingData})
#@transaction.non_atomic_requests
def index(request):
    rfidData = RfidData.objects.all()
    return render(request, 'datalog/index.html', {'RfidData':rfidData})

def datalogDB(request):  
    con = sqlite3.connect('db.sqlite3')
    #delete all data from the database first
    # 
    # gather feeding data
    feeding_data = [(1615417344,"AAA","A3",900_226000923031),
    (1615417344,"AAA","A2",900_226000923031),
    (1615417344,"AAA","A3",900_226000923031),
    (1615417344,'AAA','A4',900_226000923031),
    (1615417344,'AAA','A2',900_226000923031),
    (1615417344,'AAA','A1',900_226000923031),
    (1615417344,'AAA','A3',900_226000923031),
    (1615417344,'AAA','A1',900_226000923031),
    (1615417344,'AAA','A2',900_226000923031),
    (1615417344,'AAA','A4',900_226000923031),
    (1615417344,'AAA','A3',900_226000923031),
    (1615417344,'AAA','A3',900_226000923031),
    (1615417344,'AAA','A2',900_226000923031),
    (1615417344,'AAA','A3',900_226000923031),
    (1615417344,'AAA','A4',900_226000923031),
    (1615417344,'AAA','A2',900_226000923031),
    (1615417344,'AAA','A1',900_226000923031),
    (1615417344,'AAA','A3',900_226000923031),
    (1615417344,'AAA','A1',900_226000923031),
    (1615417344,'AAA','A2',900_226000923031),]
    for entities in feeding_data: 
        sql_insert(con, entities)

    sql_fetch(con)
    rfidData = RfidData.objects.all()
    return render(request, 'datalog/index.html',{'RfidData':rfidData})

def sql_fetch(con):

    cursorObj = con.cursor()

    cursorObj.execute('SELECT * FROM datalog_rfiddata')

    rows = cursorObj.fetchall()

    for row in rows:

        print(row)

def sql_insert(con, entities):

    cursorObj = con.cursor()
    
    cursorObj.execute('INSERT INTO datalog_rfiddata(rfid_tag_number, unix_time, site_code, feeder_id) VALUES(?, ?, ?, ?)', entities)
    
    con.commit()




