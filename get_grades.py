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
    print(
        f'{i["XNXQDM"]} [{i["KCH"]}]{i["XSKCM"]} '
        f'{i["KCXZDM_DISPLAY"]} '
        f'{i["ZCJ"] if i["ZCJ"] else "还没出成绩"} '
        f'{i["XFJD"] if i["XFJD"] else ""}'
    )
