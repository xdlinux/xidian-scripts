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

try:
    import credentials
    USERNAME = credentials.IDS_USERNAME
    PASSWORD = credentials.IDS_PASSWORD
except ImportError:
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
if '--all-terms' not in sys.argv[1:]:
    res = ses.post(
        # 查询当前学年学期和上一个学年学期
        'http://ehall.xidian.edu.cn/jwapp/sys/cjcx/modules/cjcx/cxdqxnxqhsygxnxq.do',
    ).json()['datas']['cxdqxnxqhsygxnxq']['rows']
    querySetting.append({  # 学期
        'name': 'XNXQDM',
        'value': res[-1]['XNXQDM'],
        'linkOpt': 'and',
        'builder': 'equal'
    })

total = [0, 0]
course_ignore = ['军事', '形势与政策', '创业基础', '新生', '写作与沟通', '学科导论', '心理', '物理实验']
types_ignore = ['公共任选课', '集中实践环节', '拓展提高', '通识教育核心课', '专业选修课']
unpassed_course = {}

for i in ses.post(
    'http://ehall.xidian.edu.cn/jwapp/sys/cjcx/modules/cjcx/xscjcx.do',
    data={
        'querySetting': json.dumps(querySetting),
        '*order': '+XNXQDM,KCH,KXH',
        # 请参考 https://github.com/xdlinux/xidian-scripts/wiki/EMAP#高级查询的格式
        'pageSize': 1000,
        'pageNumber': 1
    }
).json()['datas']['xscjcx']['rows']:

    flag = 0

    for lx in types_ignore:
        if i["KCLBDM_DISPLAY"].find(lx) != -1:
            flag = 1
            break

    for kw in course_ignore:
        if i["XSKCM"].find(kw) != -1:
            flag = 1
            break

    if flag == 1:
        i["XSKCM"] = '*' + i["XSKCM"]
    else:
        if i["SFJG"] == '1':  # 及格
            if i["CXCKDM"] == '01':  # 初修
                total[0] += i["XF"] * i["ZCJ"]
                total[1] += i["XF"]
            else:
                total[0] += i["XF"] * 60.0
                total[1] += i["XF"]

    if i["SFJG"] == '0' and i["KCXZDM_DISPLAY"] == "必修":
        unpassed_course[i["KCH"]] = i["XF"]
    elif i["SFJG"] == '1' and i["KCH"] in unpassed_course.keys():
        del unpassed_course[i["KCH"]]

    roman_nums = str.maketrans({
        'Ⅰ': 'I', 'Ⅱ': 'II', 'Ⅲ': 'III', 'Ⅳ': 'IV', 'Ⅴ': 'V', 'Ⅵ': 'VI', 'Ⅶ': 'VII', 'Ⅷ': 'VIII',
    }) # 一些终端无法正确打印罗马数字
    i["XSKCM"] = i["XSKCM"].translate(roman_nums)
    print(
        f'{i["XNXQDM"]} [{i["KCH"]}]{i["XSKCM"]} '
        f'{i["KCXZDM_DISPLAY"]} '
        f'{i["ZCJ"] if i["ZCJ"] else "还没出成绩"} '
        f'{i["KCLBDM_DISPLAY"]}'
    )

print(f'未获得的学分有：{sum(unpassed_course.values())}')
if '--all-terms' in sys.argv[1:]:
    print(f'加权平均成绩：{total[0] / total[1]:.2f}')
    print('注：标记有*的课程以及未通过科目不计入均分')
