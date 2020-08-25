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

import json
from libxduauth import EhallSession
try:
    import credentials
    USERNAME = credentials.IDS_USERNAME
    PASSWORD = credentials.IDS_PASSWORD
except ImportError:
    import os
    USERNAME, PASSWORD = [os.getenv(i) for i in ('IDS_USER', 'IDS_PASS')]

# Some golbal variables
sess = EhallSession(USERNAME, PASSWORD)
SERVICE_URL = 'http://ehall.xidian.edu.cn/jwapp/sys/cjcx/modules/cjcx/xscjcx.do'
querySetting = [{
        "name": "SFYX",
        "caption": "是否有效",
        "linkOpt": "AND",
        "builderList": "cbl_m_List",
        "builder": "m_value_equal",
        "value": "1",
        "value_display": "是"
    },
    {
        "name": "SHOWMAXCJ",
        "caption": "显示最高成绩",
        "linkOpt": "AND",
        "builderList": "cbl_String",
        "builder": "equal",
        "value": 0,
        "value_display": "否"
    }],


def main():
    resp = sess.post(SERVICE_URL,
        data={
            'querySetting': querySetting,
            '*order': '-XNXQDM, +KCXZDM, -XF, -KCH, -KXH', # 按照 学期、课程类型、学分、课程编号、班级编号 排序， -为降序、+为升序
            'pageSize': 1000,
            'pageNumber': 1
    })

    pretty(json.loads(resp.text))


def pretty(data):
    from prettytable import PrettyTable
    table = PrettyTable(['Course', 'Score', 'Comment', 'Credit', 'Type', 'Term'])
    courses = data['datas']['xscjcx']['rows']

    for course in courses:
        table.add_row([course['KCM'], course['ZCJ'] or '', course['QMCJ_DISPLAY'] or course['SJCJ_DISPLAY'] or '', course['XF'], course['KCXZDM_DISPLAY'], course['XNXQDM_DISPLAY']])

    table.sort_key('Type')
    print(table)


if __name__ == "__main__":
    main()