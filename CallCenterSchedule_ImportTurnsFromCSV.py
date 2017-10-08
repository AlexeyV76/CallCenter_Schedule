#CallCenterSchedule_ImportTurnsFromCSV.py
def importTurnsFromCSV(year,mon):
    import sqlite3
    import csv
    conn = sqlite3.connect('callcenter_schedule.sqlite')
    day_cur=conn.cursor()
    turn_cur=conn.cursor()
    conn.row_factory = sqlite3.Row
    for day_row in day_cur.execute('SELECT CAL_DATE, CAL_WORKD FROM CAL_V1 WHERE CAL_YEAR=? AND CAL_MON=?',(year,mon,)):
        for i in range(4 if int(day_row[1]) else 2):
            turn_cur.execute('INSERT INTO TURN(CAL_DATE,TURN_START,TURN_MAIL) VALUES(?,"09:00:00",1)',(day_row[0],))
    with open('17_11_turns.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            for day_row in day_cur.execute('SELECT CAL_DATE FROM CAL_V1 WHERE CAL_YEAR=? AND CAL_MON=? AND CAL_WORKD=?',(year,mon,int(row[2]),)):
                for i in range(int(row[1])):
                    turn_cur.execute('INSERT INTO TURN(CAL_DATE,TURN_START,TURN_MAIL) VALUES(?,?,0)',(day_row[0],row[0],))
    print(turn_cur.execute('SELECT COUNT(*) FROM TURN').fetchone()[0],'- записей импортировано.')
    conn.commit()
    conn.close()
