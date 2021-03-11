# Copyright (C) 2021 by the XiDian Open Source Community.
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

import requests
import json
import re

try:
    import credentials
    USERNAME, PASSWORD = credentials.ELECTRICITY_USERNAME, credentials.ELECTRICITY_PASSWORD
except ImportError:
    import os
    USERNAME = os.getenv('ENERGY_USER')
    PASSWORD = os.getenv('ENERGY_PASS')

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
