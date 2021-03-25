import sqlite3
# gather feeding data

#feeding_data = [('2442', '1300', 'ATE', '10'), ('2441', '1300', 'ATE', '10'), ('2440', '1400', 'ATE', '10')]

con = sqlite3.connect('db.sqlite3')

def sql_fetch(con):

    cursorObj = con.cursor()

    cursorObj.execute('SELECT * FROM datalog_feedingdata')

    rows = cursorObj.fetchall()

    for row in rows:

        print(row)

def sql_insert(con, entities):

    cursorObj = con.cursor()
    
    cursorObj.execute('INSERT INTO datalog_feedingdata(rfid_tag_number, unix_time, site_code, antenna_number) VALUES(?, ?, ?, ?)', entities)
    
    con.commit()

for entities in feeding_data: 
#entities = ('2440', '13:00', 'ATE', '10')
    sql_insert(con, entities)

sql_fetch(con)
