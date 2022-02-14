# Copyright (C) 2022 by the XiDian Open Source Community.
#
# This file is part of xidian-scripts.
#
# xidian-scripts is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# xidian-scripts is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with xidian-scripts.  If not, see <http://www.gnu.org/licenses/>.

from icalendar import Calendar, Event
from datetime import datetime, timedelta
from libxduauth import EhallSession
try:
    import credentials
    USERNAME = credentials.IDS_USERNAME
    PASSWORD = credentials.IDS_PASSWORD
except ImportError:
    import os
    USERNAME, PASSWORD = [os.getenv(i) for i in ('IDS_USER', 'IDS_PASS')]

TIME_SCHED = [
    ("8:30", "10:05"),
    ("10:25", "12:00"),
    ("14:00", "15:35"),
    ("15:55", "17:30"),
    ("19:00", "20:35")
]

ses = EhallSession(USERNAME, PASSWORD)
ses.use_app(4770397878132218)


semesterCode = ses.post(
    'http://ehall.xidian.edu.cn/jwapp/sys/wdkb/modules/jshkcb/dqxnxq.do',
    headers={
        'Accept': 'application/json, text/javascript, */*; q=0.01'
    }
).json()['datas']['dqxnxq']['rows'][0]['DM']
termStartDay = datetime.strptime(ses.post(
    'http://ehall.xidian.edu.cn/jwapp/sys/wdkb/modules/jshkcb/cxjcs.do',
    headers={
        'Accept': 'application/json, text/javascript, */*; q=0.01'
    },
    data={
        'XN': semesterCode.split('-')[0] + '-' + semesterCode.split('-')[1],
        'XQ': semesterCode.split('-')[2]
    }
).json()['datas']['cxjcs']['rows'][0]["XQKSRQ"].split(' ')[0], '%Y-%m-%d')
qResult = ses.post(
    'http://ehall.xidian.edu.cn/jwapp/sys/wdkb/modules/xskcb/xskcb.do',
    headers={  # 学生课程表
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01'
    }, data={
        'XNXQDM': semesterCode
    }
).json()
qResult = qResult['datas']['xskcb']  # 学生课程表
if qResult['extParams']['code'] != 1:
    raise Exception(qResult['extParams']['msg'])

courseList = []
for i in qResult['rows']:
    while len(courseList) < len(i['SKZC']):
        courseList.append([[], [], [], [], [], [], []])
    for j in range(len(i['SKZC'])):
        if i['SKZC'][j] == '1' and int(i['KSJC']) <= 10 and int(i['JSJC']) <= 10:
            courseList[j][int(i['SKXQ']) - 1].append({
                'name': i['KCM'],
                'location': i['JASMC'],
                'sectionSpan': (int(i['KSJC']), int(i['JSJC']))
            })

cal = Calendar()
for week_cnt in range(len(courseList)):
    for day_cnt in range(len(courseList[week_cnt])):
        for course in courseList[week_cnt][day_cnt]:
            e = Event()
            if course['sectionSpan'][0] > 10:
                continue
            elif course['location'] == None:
                course['location'] = '待定'
            e.add(
                "description",
                '课程名称：' + course['name'] +
                ';上课地点：' + course['location']
            )
            e.add('summary', course['name'] + '@' + course['location'])

            date = termStartDay + \
                timedelta(days=week_cnt * 7 + day_cnt)  # 从第一 周的第一天起
            (beginTime, endTime) = TIME_SCHED[int(course['sectionSpan'][1] / 2 - 1)]
            (beginTime, endTime) = (beginTime.split(':'), endTime.split(':'))

            e.add(
                "dtstart",
                date.replace(
                    hour=int(beginTime[0]),
                    minute=int(beginTime[1])
                )
            )
            e.add(
                "dtend",
                date.replace(
                    hour=int(endTime[0]),
                    minute=int(endTime[1])
                )
            )
            cal.add_component(e)
f = open(USERNAME + '_' + semesterCode + ".ics", 'wb')
f.write(cal.to_ical())
f.close()
print("日历文件已保存到 " + USERNAME + '_' + semesterCode + ".ics")
