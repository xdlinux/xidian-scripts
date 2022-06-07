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

USERNAME, PASSWORD = [os.getenv(i) for i in ('ENERGY_USER', 'ENERGY_PASS')]
if not USERNAME or not PASSWORD:
    print('请设置环境变量 ENERGY_USER 和 ENERGY_PASS')
    exit(1)


import re
from libxduauth import EnergySession

ses = EnergySession(USERNAME, PASSWORD)

balance_page = ses.get(
    'http://10.168.55.50:8088/searchWap/webFrm/met.aspx'
).text
pattern_name = re.compile('表名称：(.*?)  ', re.S)
name = re.findall(pattern_name, balance_page)
pattern_balance = re.compile('剩余量：(.*?) </td>', re.S)
balance = re.findall(pattern_balance, balance_page)
print("电费账号：", USERNAME)
for n, b in zip(name, balance):
    print(" 表名称：", n, "剩余量：", float(b))
