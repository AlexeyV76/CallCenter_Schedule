from datetime import datetime, date, time, timedelta
import sqlite3
conn = sqlite3.connect('callcenter_schedule.sqlite')
day_cur=conn.cursor()
per_cur=conn.cursor()
turn_cur=conn.cursor()
conn.row_factory = sqlite3.Row
year = str(date.today().year)
mon = "11"
roles=("Супервизор","Оператор","Новичок",)
data=[
    '    <table>',
    '      <thead>',
    '        <tr>',
    '          <th>Сотрудник</th>',]
for day_row in day_cur.execute('SELECT * FROM CAL_V1 WHERE CAL_YEAR=? AND CAL_MON=?', (year,mon,)):
    dattmp='          <th>'+str(day_row[0])+'<br>'+str(day_row[6])+'</th>'
    data.append(dattmp)
data.append('        </tr>')
data.append('      </thead>')
data.append('      <tbody>')
for per_row in per_cur.execute('SELECT * FROM PERSONS_FULL'):
    data.append('        <tr>')
    dattmp='          <td class="firstcol">'+str(per_row[1])+'</td>'
    data.append(dattmp)
    for day_row in day_cur.execute('SELECT * FROM CAL_V1 WHERE CAL_YEAR=? AND CAL_MON=?', (year,mon,)):
        t=turn_cur.execute('SELECT * FROM TURN_FULL WHERE PER=? AND DATE=?', (per_row[1],day_row[0])).fetchall()
        dattmp='          <td id="'+(per_row[1]+','+day_row[0] if len(t)==0 else str(t[0][0]))+'" onclick="ChChange(this.id);">'+("<BR><BR><BR>" if len(t)==0 else str(t[0][8])+" 8ч."+("<BR>Обработка почты" if t[0][10] else "<BR><BR>"))+'</td>'
        data.append(dattmp)
    data.append('        </tr>')
data.append('      </tbody>')
data.append('    </table>')
with open('CallCenterSchedule.html','w', encoding='windows-1251') as resultFile:
    for s in data:
        print(s, file=resultFile)
conn.close()
