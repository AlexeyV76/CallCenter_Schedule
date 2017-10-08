import sqlite3, os, csv, sys, re, subprocess
out_csv = 'res.csv'
conn = sqlite3.connect('callcenter_schedule.sqlite')
per_cur=conn.cursor()
SQL_Check="""
SELECT
  (SELECT PER
   FROM TURN_FULL
   WHERE OID=?),
  (SELECT DATE||' '||TS
   FROM TURN_FULL
   WHERE OID=?),
  ((SELECT strftime('%s',DATE||' '||TS)
   FROM TURN_FULL
   WHERE OID=?)/3600
- (SELECT strftime('%s',DATE||' '||TS)
   FROM TURN_FULL
   WHERE DATE=(SELECT MAX(DATE)
               FROM TURN_FULL
               WHERE DATE<(SELECT DATE
                           FROM TURN_FULL
                           WHERE OID=?)
               AND PER=(SELECT PER
                        FROM TURN_FULL
                        WHERE OID=?))
   AND PER=(SELECT PER
            FROM TURN_FULL
            WHERE OID=?)
   )/3600
- 9 - 12)>=0
AND
  ((SELECT strftime('%s',DATE||' '||TS)
   FROM TURN_FULL
   WHERE DATE=(SELECT MIN(DATE)
               FROM TURN_FULL
               WHERE DATE>(SELECT DATE
                           FROM TURN_FULL
                           WHERE OID=?)
               AND PER=(SELECT PER
                        FROM TURN_FULL
                        WHERE OID=?))
   AND PER=(SELECT PER
            FROM TURN_FULL
            WHERE OID=?)
   )/3600
- (SELECT strftime('%s',DATE||' '||TS)
   FROM TURN_FULL
   WHERE OID=?)/3600
- 9 - 12)>=0;
"""
SQL_Check_Same="""
SELECT DATE
FROM TURN_FULL
WHERE DATE=(SELECT DATE
            FROM TURN_FULL
            WHERE OID=?)
AND PER=(SELECT PER
         FROM TURN_FULL
         WHERE OID=?);
"""
SQL_Update="""
UPDATE TURN
SET PER_ID=?
WHERE OID=?;
"""
t1=sys.argv[1]
t2=sys.argv[2]
r1=per_cur.execute(SQL_Check, (t2,t1,t1,t1,t2,t2,t1,t2,t2,t1)).fetchone()
r11=len(per_cur.execute(SQL_Check_Same,(t1,t2)).fetchall())
r2=per_cur.execute(SQL_Check, (t1,t2,t2,t2,t1,t1,t2,t1,t1,t2)).fetchone()
r21=len(per_cur.execute(SQL_Check_Same,(t2,t1)).fetchall())
with open(out_csv, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow([r1[0],r1[1],r1[2],r11])
    csvwriter.writerow([r2[0],r2[1],r2[2],r21])
csvfile.close()
b=False
if r1[2] and r2[2]:
    if re.split('\ ',r1[1])[0]==re.split('\ ',r2[1])[0]:
        b=True 
    elif (not r11) and (not r21):
        b=True
if b:
    p=[(r1[0],t1),
       (r2[0],t2)]
    per_cur.executemany(SQL_Update,p)
    conn.commit()
    subprocess.run(['python','CallCenterSchedule_ExportHTML.py'])
conn.close()