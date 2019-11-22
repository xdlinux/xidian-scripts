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

import requests
import json
import re
import credentials

USERNAME = credentials.ELECTRICITY_USERNAME
PASSWORD = credentials.ELECTRICITY_PASSWORD

login_page = requests.get("http://10.168.55.50:8088/searchWap/Login.aspx")
cookies_login = login_page.cookies
post_data = {
    "webName": USERNAME,
    "webPass": PASSWORD
}

HEADER = {
    "AjaxPro-Method": "getLoginInput",
    'Host': '10.168.55.50:8088',
    'Connection': 'keep-alive',
    'Origin': 'http://10.168.55.50:8088'
}
login_result = requests.post(
    "http://10.168.55.50:8088/ajaxpro/SearchWap_Login,App_Web_fghipt60.ashx",
    data=json.dumps(post_data), cookies=cookies_login, headers=HEADER
)

balance_page = requests.get(
    'http://10.168.55.50:8088/searchWap/webFrm/met.aspx', cookies=cookies_login
)

pattern_name = re.compile('表名称：(.*?)  ', re.S)
name = re.findall(pattern_name, balance_page.text)
pattern_balance = re.compile('剩余量：(.*?) </td>', re.S)
balance = re.findall(pattern_balance, balance_page.text)
print("电费账号：", USERNAME)
for n, b in zip(name, balance):
    print(" 表名称：", n, "剩余量：", float(b))
