from datetime import datetime, date, time, timedelta
import sqlite3
import random
import CallCenterSchedule_ImportTurnsFromCSV
from random import choices
year = str(date.today().year)
mon = "11"
CallCenterSchedule_ImportTurnsFromCSV.importTurnsFromCSV(year,mon)
conn = sqlite3.connect('callcenter_schedule.sqlite')
mon_cur = conn.cursor()
turn_cur = conn.cursor()
per_turn_cur = conn.cursor()
per_sel_cur = conn.cursor()
conn.row_factory = sqlite3.Row
roles=("Супервизор","Оператор","Новичок",)
SQL="FROM PER_PLAN_FULL WHERE PLAN_MON=? AND D=? AND P2C_HOL=0 AND PL_REM>0 AND (strftime('%s',?)-strftime('%s',LAST_END))>=(12*3600) "
SQL_turns="""
SELECT TS
FROM TURN_FULL_TO_FILL
WHERE (YEAR=?) AND (MON=?) AND (DAY=?) AND (TS!=?)
GROUP BY TS"""
turns_first=("05:00:00","14:00:00",)
turn_last="09:00:00"
superv_turns=["05:00:00","14:00:00"]
for mon_row in mon_cur.execute('SELECT * FROM CAL_V1 WHERE (CAL_YEAR=?) AND (CAL_MON=?)', (year,mon,)):
    for turn in turns_first:
        per_turn_row=per_turn_cur.execute('SELECT * FROM TURN_FULL_TO_FILL WHERE (YEAR=?) AND (MON=?) AND (DAY=?) AND (TS=?)', (year,mon,mon_row[3],turn,)).fetchone()
        r_text="AND PER_DOL=?"
        p_sc=(mon,mon_row[3],year+"-"+mon+"-"+mon_row[3]+" "+turn,roles[0])
        per_sel_cur.execute("SELECT max(PL_MAX) "+SQL+r_text,p_sc)
        p_sc=(per_sel_cur.fetchone()[0],mon,mon_row[3],year+"-"+mon+"-"+mon_row[3]+" "+turn,roles[0],)
        per_sel_cur.execute("SELECT PER, ?-PL_MAX+PL_REM, PER_DOL "+SQL+r_text,p_sc)
        per_to_choose=[[],[],]
        for t in per_sel_cur.fetchall():
            per_to_choose[0].append(t[0])
            per_to_choose[1].append(t[1]**3)
        per_temp=random.choices(per_to_choose[0],per_to_choose[1])[0]
        eoft=(datetime.strptime(year+mon+mon_row[3]+per_turn_row[8],"%Y%m%d%H:%M:%S")+timedelta(hours=9)).isoformat(" ","seconds")
        per_sel_cur.execute("""UPDATE PER_PLAN
            SET PER_PL_REM=(SELECT PER_PL_REM-1 FROM PER_PLAN WHERE PER_PLAN_MONTH=? AND PER_ID=?), PER_PL_LAST_END=?
            WHERE PER_PLAN_MONTH=? AND PER_ID=?;""", (mon,per_temp,eoft,mon,per_temp,))
        per_sel_cur.execute("UPDATE TURN SET PER_ID=? WHERE OID=?;", (per_temp,per_turn_row[0],))
        conn.commit()
    for turn_row in turn_cur.execute(SQL_turns, (year,mon,mon_row[3],turn_last,)):
        for per_turn_row in per_turn_cur.execute('SELECT * FROM TURN_FULL_TO_FILL WHERE (YEAR=?) AND (MON=?) AND (DAY=?) AND (TS=?)', (year,mon,mon_row[3],turn_row[0],)):
            p_sc=(mon,mon_row[3],year+"-"+mon+"-"+mon_row[3]+" "+turn_row[0],roles[2],)
            r_text="AND PER_DOL!=?"
            per_sel_cur.execute("SELECT max(PL_MAX) "+SQL+r_text,p_sc)
            p_sc=(per_sel_cur.fetchone()[0],mon,mon_row[3],year+"-"+mon+"-"+mon_row[3]+" "+turn_row[0],roles[2],)
            per_sel_cur.execute("SELECT PER, ?-PL_MAX+PL_REM, PER_DOL "+SQL+r_text,p_sc)
            per_to_choose=[[],[],]
            for t in per_sel_cur.fetchall():
                per_to_choose[0].append(t[0])
                per_to_choose[1].append(t[1]**3)
            per_temp=random.choices(per_to_choose[0],per_to_choose[1])[0]
            eoft=(datetime.strptime(year+mon+mon_row[3]+per_turn_row[8],"%Y%m%d%H:%M:%S")+timedelta(hours=9)).isoformat(" ","seconds")
            per_sel_cur.execute("""UPDATE PER_PLAN
                SET PER_PL_REM=(SELECT PER_PL_REM-1 FROM PER_PLAN WHERE PER_PLAN_MONTH=? AND PER_ID=?), PER_PL_LAST_END=?
                WHERE PER_PLAN_MONTH=? AND PER_ID=?;""", (mon,per_temp,eoft,mon,per_temp,))
            per_sel_cur.execute("UPDATE TURN SET PER_ID=? WHERE OID=?;", (per_temp,per_turn_row[0],))
            conn.commit()
    for  per_turn_row in per_turn_cur.execute('SELECT * FROM TURN_FULL_TO_FILL WHERE (YEAR=?) AND (MON=?) AND (DAY=?) AND (TS=?) AND (MAIL=1)', (year,mon,mon_row[3],turn_last,)):
        p_sc=(mon,mon_row[3],year+"-"+mon+"-"+mon_row[3]+" "+turn_last,roles[2])
        r_text="AND PER_DOL!=?"
        per_sel_cur.execute("SELECT max(PL_MAX) "+SQL+r_text,p_sc)
        p_sc=(per_sel_cur.fetchone()[0],mon,mon_row[3],year+"-"+mon+"-"+mon_row[3]+" "+turn_last,roles[2])
        per_sel_cur.execute("SELECT PER, ?-PL_MAX+PL_REM, PER_DOL "+SQL+r_text,p_sc)
        per_to_choose=[[],[],]
        for t in per_sel_cur.fetchall():
            per_to_choose[0].append(t[0])
            per_to_choose[1].append(t[1]**3)
        per_temp=random.choices(per_to_choose[0],per_to_choose[1])[0]
        eoft=(datetime.strptime(year+mon+mon_row[3]+per_turn_row[8],"%Y%m%d%H:%M:%S")+timedelta(hours=9)).isoformat(" ","seconds")
        per_sel_cur.execute("""UPDATE PER_PLAN
            SET PER_PL_REM=(SELECT PER_PL_REM-1 FROM PER_PLAN WHERE PER_PLAN_MONTH=? AND PER_ID=?), PER_PL_LAST_END=?
            WHERE PER_PLAN_MONTH=? AND PER_ID=?;""", (mon,per_temp,eoft,mon,per_temp,))
        per_sel_cur.execute("UPDATE TURN SET PER_ID=? WHERE OID=?;", (per_temp,per_turn_row[0],))
        conn.commit()
    for  per_turn_row in per_turn_cur.execute('SELECT * FROM TURN_FULL_TO_FILL WHERE (YEAR=?) AND (MON=?) AND (DAY=?) AND (TS=?) AND (MAIL=0)', (year,mon,mon_row[3],turn_last,)):
        p_sc=(mon,mon_row[3],year+"-"+mon+"-"+mon_row[3]+" "+turn_last,)
        per_sel_cur.execute("SELECT max(PL_MAX) "+SQL,p_sc)
        p_sc=(per_sel_cur.fetchone()[0],mon,mon_row[3],year+"-"+mon+"-"+mon_row[3]+" "+turn_last,)
        per_sel_cur.execute("SELECT PER, ?-PL_MAX+PL_REM, PER_DOL "+SQL,p_sc)
        per_to_choose=[[],[],]
        for t in per_sel_cur.fetchall():
            per_to_choose[0].append(t[0])
            per_to_choose[1].append(t[1]**2 if t[2]!=roles[2] else t[1]**4)
        per_temp=random.choices(per_to_choose[0],per_to_choose[1])[0]
        eoft=(datetime.strptime(year+mon+mon_row[3]+per_turn_row[8],"%Y%m%d%H:%M:%S")+timedelta(hours=9)).isoformat(" ","seconds")
        per_sel_cur.execute("""UPDATE PER_PLAN
            SET PER_PL_REM=(SELECT PER_PL_REM-1 FROM PER_PLAN WHERE PER_PLAN_MONTH=? AND PER_ID=?), PER_PL_LAST_END=?
            WHERE PER_PLAN_MONTH=? AND PER_ID=?;""", (mon,per_temp,eoft,mon,per_temp,))
        per_sel_cur.execute("UPDATE TURN SET PER_ID=? WHERE OID=?;", (per_temp,per_turn_row[0],))
        conn.commit()
conn.rollback()
conn.close()
