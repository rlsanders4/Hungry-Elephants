from django.shortcuts import render
from django.http import HttpResponse
from .models import FeedingData
from .models import RFIDLogData
import csv  
import sqlite3

def feedingdata(request):
    feedingData = FeedingData.objects.all()
    return render(request, 'datalog/feedingdata.html', {'FeedingData':feedingData})

def index(request):
    rfidLogData = RFIDLogData.objects.all()
    return render(request, 'datalog/index.html', {'RfidLogData':rfidLogData})
def rfiddata(request):
    rfidLogData = RFIDLogData.objects.all()
    return render(request, 'datalog/index.html', {'RfidLogData':rfidLogData})

def getRfidFile(request):  
    response = HttpResponse(content_type='text/csv')  
    response['Content-Disposition'] = 'attachment; filename="RFIDLogData.csv"'  
    rfidData = RFIDLogData.objects.all()  
    writer = csv.writer(response)  
    for rfid in rfidData:  
        writer.writerow([rfid.unix_time,rfid.site_code, rfid.antenna_tag, rfid.rfid])  
    return response 

def getCompletedTaskFile(request):  
    response = HttpResponse(content_type='text/csv')  
    response['Content-Disposition'] = 'attachment; filename="completedTask.csv"'  
    feedingDatas = FeedingData.objects.all()  
    writer = csv.writer(response)  
    for feed in feedingDatas:  
        writer.writerow([feed.task_uuid,feed.execute_after_UNIX_time,feed.target_site_code, feed.target_feeder_number,
                        feed.amount, feed.if_recieve_from_antenna_number, feed.if_recieve_from_tag_number, feed.interval_time,
                        feed.expire_time, feed.repeat_X_times, feed.completed_time])  
    return response  


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




