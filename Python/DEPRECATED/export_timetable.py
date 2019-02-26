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
from datetime import timedelta
from datetime import datetime
import auth.ids
import configurations
import credentials

TIMETABLE_URL = "https://xidian.cpdaily.com/comapp-timetable/sys/schoolTimetable/v2/api/weekTimetable"

END_MONTH = 5  # Month when timetable is changed in summer
END_DAY = 2  # Day when timetable is changed in summer
# Use for ehall data source
TERM = 2  # Current term (1 / 2)
TERM_START_DAY = datetime(2019, 2, 25)  # Day when term starts

if __name__ == '__main__':
    # Time A(summer)
    section_start_time_a = ["08:00", "08:30", "09:20", "10:25", "11:15",  # morning
                            "14:30", "15:20", "16:25", "17:15",  # afternoon
                            "19:30", "20:20"]  # evening
    section_end_time_a = ["08:30", "09:15", "10:05", "11:10", "12:00",
                          "15:15", "16:05", "17:10", "18:00",
                          "20:15", "21:05"]

    # Time B(spring, autumn and winter)
    section_start_time_b = ["08:00", "08:30", "09:20", "10:25", "11:15",
                            "14:00", "14:50", "15:55", "16:45",
                            "19:00", "19:50"]
    section_end_time_b = ["08:30", "09:15", "10:05", "11:10", "12:00",
                          "14:45", "15:35", "16:40", "17:30",
                          "19:45", "20:35"]
    print("注意: \n1. 未排时间的课不会显示在课表中\n2. 如果今日校园数据源无法获取，请使用一站式服务大厅数据源")
    print()
    print("请选择数据来源 (1/2):")
    print("1. 今日校园")
    print("2. 一站式服务大厅")
    source = input()
    if source == "1":
        ses = auth.ids.get_login_session(TIMETABLE_URL, credentials.IDS_USERNAME, credentials.IDS_PASSWORD)
        ses.get(TIMETABLE_URL)
        result = ses.get(TIMETABLE_URL).json()
        if result["code"] != '0':
            print(result['message'])
        else:
            allteachweeks = result["allTeachWeeks"]
            cal = Calendar()
            for current_week in result["termWeeksCourse"]:
                for current_day in current_week["courses"]:
                    if len(current_day["sectionCourses"]) != 0:
                        course_day = current_day["date"]
                        for current_course in current_day["sectionCourses"]:
                            course_name = current_course["courseName"]
                            course_classroom = current_course["classroom"]
                            course_start_number = current_course["sectionStart"]
                            course_end_number = current_course["sectionEnd"]
                            event = Event()
                            day_1 = datetime.strptime(course_day, "%Y-%m-%d")  # Course day
                            day_2 = datetime(
                                configurations.SCHOOL_YEAR[0], 10, 8)  # Semester 1
                            day_3 = datetime(
                                configurations.SCHOOL_YEAR[1], END_MONTH, END_DAY)  # Semester 2
                            event.add("description", course_name + " @ " + course_classroom)
                            event.add("summary", course_name + " @ " + course_classroom)
                            if day_2 < day_1 < day_3:
                                event.add("dtstart", datetime.strptime(
                                    course_day + " " + section_start_time_b[int(course_start_number)],
                                    "%Y-%m-%d %H:%M"))
                                event.add("dtend", datetime.strptime(
                                    course_day + " " + section_end_time_b[int(course_end_number)], "%Y-%m-%d %H:%M"))
                            else:
                                event.add("dtstart", datetime.strptime(
                                    course_day + " " + section_start_time_a[int(course_start_number)],
                                    "%Y-%m-%d %H:%M"))
                                event.add("dtend", datetime.strptime(
                                    course_day + " " + section_end_time_a[int(course_end_number)], "%Y-%m-%d %H:%M"))
                            cal.add_component(event)
            f = open(credentials.IDS_USERNAME + '_' + result["yearTerm"] + ".ics", 'wb')
            f.write(cal.to_ical())
            f.close()
            print("日历文件已保存到 " + credentials.IDS_USERNAME + '_' + result["yearTerm"] + ".ics")
    elif source == "2":
        ses = auth.ids.get_login_session('http://ehall.xidian.edu.cn:80//appShow', credentials.IDS_USERNAME,
                                         credentials.IDS_PASSWORD)
        ses.get('http://ehall.xidian.edu.cn//appShow?appId=4770397878132218', headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        })
        result = ses.post('http://ehall.xidian.edu.cn/jwapp/sys/wdkb/modules/xskcb/xskcb.do', headers={  # 学生课程表
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01'
        }, data={'XNXQDM': '2018-2019-2'}).json()
        cal = Calendar()
        for i in result['datas']['xskcb']['rows']:
            for j in range(len(i['SKZC'])):
                if i['SKZC'][j] == '1':
                    course_name = i["KCM"]
                    course_classroom = i["JASMC"]
                    course_day = TERM_START_DAY + timedelta(days=int(j) * 7 + int(i["SKXQ"]) - 1)
                    course_start_number = i["KSJC"]
                    course_end_number = i["JSJC"]
                    event = Event()
                    day_1 = course_day  # Course day
                    day_2 = datetime(configurations.SCHOOL_YEAR[0], 10, 8)  # Semester 1
                    day_3 = datetime(configurations.SCHOOL_YEAR[1], END_MONTH, END_DAY)  # Semester 2
                    event.add("description", course_name + " @ " + course_classroom)
                    event.add("summary", course_name + " @ " + course_classroom)
                    if day_2 < day_1 < day_3:
                        event.add("dtstart", datetime.strptime(
                            datetime.strftime(course_day, "%Y-%m-%d") + " " + section_start_time_b[
                                int(course_start_number)],
                            "%Y-%m-%d %H:%M"))
                        event.add("dtend", datetime.strptime(
                            datetime.strftime(course_day, "%Y-%m-%d") + " " + section_end_time_b[
                                int(course_end_number)], "%Y-%m-%d %H:%M"))
                    else:
                        event.add("dtstart", datetime.strptime(
                            datetime.strftime(course_day, "%Y-%m-%d") + " " + section_start_time_a[
                                int(course_start_number)],
                            "%Y-%m-%d %H:%M"))
                        event.add("dtend", datetime.strptime(
                            datetime.strftime(course_day, "%Y-%m-%d") + " " + section_end_time_a[
                                int(course_end_number)], "%Y-%m-%d %H:%M"))
                    cal.add_component(event)
        f = open(credentials.IDS_USERNAME + '_' + result["datas"]["xskcb"]["rows"][0]["XNXQDM"] + ".ics", 'wb')
        f.write(cal.to_ical())
        f.close()
        print("日历文件已保存到 " + credentials.IDS_USERNAME + '_' + result["datas"]["xskcb"]["rows"][0]["XNXQDM"] + ".ics")
