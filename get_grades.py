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

import pkg_resources
import subprocess
import sys
import os
try:
    pkg_resources.require(('libxduauth'))
except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
    subprocess.check_call([
        sys.executable, '-m', 'pip', 'install', 'libxduauth'
    ])

USERNAME, PASSWORD = [os.getenv(i) for i in ('IDS_USER', 'IDS_PASS')]
if not USERNAME or not PASSWORD:
    print('请设置环境变量 IDS_USER 和 IDS_PASS')
    exit(1)

import json
import sys
from libxduauth import EhallSession

ses = EhallSession(USERNAME, PASSWORD)
ses.use_app(4768574631264620)

querySetting = [
    {  # 是否有效
        'name': 'SFYX',
        'value': '1',
        'linkOpt': 'and',
        'builder': 'm_value_equal'
    }
]
if '--current-term' in sys.argv[1:]:
    res = ses.post(
        # 查询当前学年学期hsyg学年学期
        'http://ehall.xidian.edu.cn/jwapp/sys/cjcx/modules/cjcx/cxdqxnxqhsygxnxq.do',
    ).json()['datas']['cxdqxnxqhsygxnxq']['rows']
    querySetting.append({  # 学期
        'name': 'XNXQDM',
        'value': res[0]['XNXQDM'],
        'linkOpt': 'and',
        'builder': 'equal'
    })
# 请参考 https://github.com/xdlinux/xidian-scripts/wiki/EMAP#高级查询的格式
courses = {}

for i in ses.post(
    'http://ehall.xidian.edu.cn/jwapp/sys/cjcx/modules/cjcx/xscjcx.do',
    data={
        'querySetting': json.dumps(querySetting),
        '*order': 'KCH,KXH',  # 按课程名，课程号排序
        'pageSize': 1000,  # 有多少整多少.jpg
        'pageNumber': 1
    }
).json()['datas']['xscjcx']['rows']:
    if i['XNXQDM_DISPLAY'] not in courses.keys():
        courses[i['XNXQDM_DISPLAY']] = []
    courses[i['XNXQDM_DISPLAY']].append(
        (i['XSKCM'].strip(), str(i['ZCJ']), str(i['XFJD'])))

for i in courses.keys():
    print(i + ':')
    for j in courses[i]:
        if j[2] == 'None':
            print('\t' + j[0] + ': ' + j[1])
        else:
            print('\t' + j[0] + ': ' + j[1] + ' (' + j[2] + ')')
