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

import re
import credentials
from libxduauth import ZFWSession
import bs4

try:
    import credentials
    USERNAME = credentials.PAY_USERNAME
    PASSWORD = credentials.PAY_PASSWORD
except:
    import os
    USERNAME, PASSWORD = [os.getenv(i) for i in ('PAY_USER', 'PAY_PASS')]


def get_info(ses):
    info_url = ses.BASE + '/home'
    ip_list = []
    used = ""
    rest = ""
    charged = ""
    filt = re.compile(r'>(.*)<')
    soup = bs4.BeautifulSoup(ses.get(info_url).text, 'lxml')
    tr_list = soup.find_all('tr')
    for tr in tr_list:
        td_list = bs4.BeautifulSoup(str(tr), 'lxml').find_all('td')
        if len(td_list) == 0:
            continue
        elif len(td_list) == 4:
            ip = filt.search(str(td_list[0])).group(1)
            online_time = filt.search(str(td_list[1])).group(1)
            used_t = filt.search(str(td_list[2])).group(1)
            if used_t == '':
                continue
            ip_list.append((ip, online_time, used_t))
        elif len(td_list) == 6:
            used = filt.search(str(td_list[1])).group(1)
            rest = filt.search(str(td_list[2])).group(1)
            charged = filt.search(str(td_list[3])).group(1)
    return ip_list, used, rest, charged


if __name__ == '__main__':
    ses = ZFWSession(USERNAME, PASSWORD)
    ip_list, used, rest, charged = get_info(ses)
    for ip_info in ip_list:
        print(ip_info)
    print("此月已使用流量 %s , 剩余 %s , 充值剩余 %s" % (used, rest, charged))
