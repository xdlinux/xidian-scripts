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
import requests
import re
import configurations
import credentials

expList = []


def get_experiments():
    global semesterCode, expList
    expList.clear()
    ses = requests.session()
    ses.post('http://wlsy.xidian.edu.cn/PhyEws/default.aspx',
             data={
                 '__EVENTTARGET': '',
                 '__EVENTARGUMENT': '',
                 '__VIEWSTATE': '/wEPDwUKMTEzNzM0MjM0OWQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFD2xvZ2luMSRidG5Mb2dpbutGpJNAAaBhxseXkh1n/woLBppW',
                 '__VIEWSTATEGENERATOR': 'EE008CD9',
                 '__EVENTVALIDATION': '/wEWBwLsvJu+AgKckJOGDgKD8YXRCQLJ5dDDBAKVx8n1CQKytMi0AQKcg465CqDdcB40IuBzviNuzXl4xNRdD759',
                 'login1$StuLoginID': credentials.PHYSICS_USERNAME,
                 'login1$StuPassword': credentials.PHYSICS_PASSWORD,
                 'login1$UserRole': 'Student',
                 'login1$btnLogin.x': '0',
                 'login1$btnLogin.y': '0'
             })
    html = ses.get('http://wlsy.xidian.edu.cn/PhyEws/student/select.aspx')

    pattern = re.compile(
        r'<td class="forumRow" height="25"><a class="linkSmallBold"(.*?)target="_new">((?!《物理实验》)(?!下载).*?)（[0-9]学时）</a></td>'
        r'<td class="forumRow" align="center" height="25"><span>[0-9]{1,2}</span></td>'
        r'<td class="forumRow" height="25"><span>星期(.*?)((([01][0-9]|2[0-3]):[0-5][0-9])\-(([01][0-9]|2[0-3]):[0-5][0-9]))</span></td>'
        r'<td class="forumRow" height="25"><span>([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})</span></td>'
        r'<td class="forumRow" align="center" height="25"><span>([A-F]([0-999]{3,3}))</span></td>')
    result = pattern.findall(html.text)
    for exp in result:
        expName = exp[1]
        expStart = exp[4]
        expEnd = exp[6]
        expDate = exp[8]
        expClassroom = exp[9]
        expList.append([expName, expStart, expEnd, expDate, expClassroom])


source = input("请确保当前处于校园网或翼讯网络环境下，回车继续...")
get_experiments()
cal = Calendar()
for exp in expList:
    e = Event()
    e.add("description", exp[0] + ' @ ' + exp[4])
    e.add('summary', exp[0] + ' @ ' + exp[4])
    start = datetime.strptime(exp[3] + ' ' + exp[1], '%m/%d/%Y %H:%M')
    e.add('dtstart', start)
    end = datetime.strptime(exp[3] + ' ' + exp[2], '%m/%d/%Y %H:%M')
    e.add('dtend', end)
    e.add('location', exp[4])
    cal.add_component(e)

f = open(credentials.IDS_USERNAME + '_physicsExperiment.ics', 'wb')
f.write(cal.to_ical())
f.close()
print("物理实验日历文件已保存到 " + credentials.IDS_USERNAME + '_physicsExperiment.ics')
