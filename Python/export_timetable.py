# Copyright (C) 2019 by the XiDian Open Source Community.
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
import auth.ids
import configurations
import credentials

courseList = []
semesterCode = ''

MORNING_TIME = [
    ("8:30", "10:05"),
    ("10:25", "12:00")
]
SUMMER_TIME = MORNING_TIME + [
    ("14:30", "16:05"),
    ("16:25", "18:00"),
    ("19:30", "21:05")
]
WINTER_TIME = MORNING_TIME + [
    ("14:00", "15:35"),
    ("15:55", "17:30"),
    ("19:00", "20:35")
]


def get_courses_from_dcampus():
    global semesterCode, courseList
    courseList.clear()
    ses = auth.ids.get_login_session(
        'https://xidian.cpdaily.com',
        credentials.IDS_USERNAME,
        credentials.IDS_PASSWORD
    )
    qResult = ses.get('https://xidian.cpdaily.com/comapp-timetable/sys/schoolTimetable/v2/api/weekTimetable').json()
    if qResult['code'] != '0':
        raise Exception(qResult['message'])
    semesterCode = qResult['yearTerm']
    # allTeachWeeks = qResult['allTeachWeeks'] #教学周数
    for week in qResult['termWeeksCourse']:
        courseList.append([])
        t = courseList[-1]
        for day in week['courses']:
            for Class in day['sectionCourses']:
                t.append({
                    'name': Class['courseName'],
                    'location': Class['classroom'],
                    'sectionSpan': (
                        Class['sectionStart'],
                        Class['sectionEnd']
                    )
                })


def get_courses_from_ehall():
    global semesterCode, courseList
    courseList.clear()
    # 换校历的话可能要改, 不换就没事
    ses = auth.ids.get_login_session(
        'http://ehall.xidian.edu.cn:80//appShow',
        credentials.IDS_USERNAME,
        credentials.IDS_PASSWORD
    )
    ses.get('http://ehall.xidian.edu.cn//appShow?appId=4770397878132218', headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    })

    if configurations.USE_LATEST_SEMESTER:
        semesterCode = ses.post(
            'http://ehall.xidian.edu.cn/jwapp/sys/wdkb/modules/jshkcb/dqxnxq.do',
            headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01'
            }
        ).json()['datas']['dqxnxq']['rows'][0]['DM']
        global termStartDay
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
    else:
        semesterCode = \
            str(configurations.SCHOOL_YEAR[0]) + '-' + \
            str(configurations.SCHOOL_YEAR[1]) + '-' + \
            str(configurations.SEMESTER)
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

    for i in qResult['rows']:
        while len(courseList) < len(i['SKZC']):
            courseList.append([[], [], [], [], [], [], []])
        for j in range(len(i['SKZC'])):
            if i['SKZC'][j] == '1':
                courseList[j][int(i['SKXQ']) - 1].append({
                    'name': i['KCM'],
                    'location': i['JASMC'],
                    'sectionSpan': (int(i['KSJC']), int(i['JSJC']))
                })


source = input("请选择数据来源 (1/2):\n1. 今日校园\n2. 一站式服务大厅\n>")
if source == '1':
    get_courses_from_dcampus()
elif source == '2':
    get_courses_from_ehall()

cal = Calendar()
for week_cnt in range(len(courseList)):
    for day_cnt in range(len(courseList[week_cnt])):
        for course in courseList[week_cnt][day_cnt]:
            e = Event()
            if course['sectionSpan'][0] > 10 :
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
            (beginTime, endTime) = \
                SUMMER_TIME[int(course['sectionSpan'][1] / 2 - 1)] if \
                    date.month >= 5 and date.month < 10 else \
                    WINTER_TIME[int(course['sectionSpan'][1] / 2 - 1)]
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
f = open(credentials.IDS_USERNAME + '_' + semesterCode + ".ics", 'wb')
f.write(cal.to_ical())
f.close()
print("日历文件已保存到 " + credentials.IDS_USERNAME + '_' + semesterCode + ".ics")
