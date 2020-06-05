# Copyright (C) 2020 by the XiDian Open Source Community.
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

# python3，需要requests和BeautifulSoup4
import time
import requests
from bs4 import BeautifulSoup

from libxduauth import RSBBSSession
try:
    import credentials
    USERNAME, PASSWORD = credentials.RS_USERNAME, credentials.RS_PASSWORD
except ImportError:
    import os
    USERNAME = os.getenv('RS_USER')
    PASSWORD = os.getenv('RS_PASS')

ses = RSBBSSession(USERNAME, PASSWORD)


def get_hr_posts():
    # 外网睿思rsbbs
    response = ses.get('http://rsbbs.xidian.edu.cn/forum.php', params={
        'mod': 'forumdisplay', 'fid': '554', 'filter': 'typeid', 'typeid': '43'
    })
    html = BeautifulSoup(response.text, 'html.parser')
    info_all = {}
    hr_index = 1
    for link in html.find_all('li'):
        link = link.find('a')
        info_link = link.get('href')
        # del 就业招聘版版规
        if "921702" in info_link:
            continue
        info_link = "http://rsbbs.xidian.edu.cn/" + info_link
        info_text = link.get_text(strip=True)
        info_all[info_text] = info_link
        hr_index += 1
    return hr_index, info_all

import sys
options = sys.argv[1:]
if __name__ == '__main__':
    template = '{k}:\t{v}  \n'
    if '--markdown' in options:
        template = '[{k}]({v})  \n'
    first_hr, info_all = get_hr_posts()
    first_hr_new = first_hr
    desp_data = ''
    for k, v in info_all.items():
        desp_data += template.format(k=k, v=v)

    if '--urlencode' in options:
        from urllib import parse
        desp_data = parse.quote(desp_data)
    print(desp_data)
