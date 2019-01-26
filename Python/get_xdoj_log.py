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

import random
import re
import os
import sys
import requests
import credentials

base = 'http://202.117.120.31/xdoj/'
contests = []
res = []
regex_filename = r"<tr bgcolor=\"#[ef]{6}\">[\r\n\t]*[^`]*?<font color=(\w*)>[^`]*?download_source\('(\w*)'\)[^`]*?<\/tr>"
regex_contest  = r"href='/xdoj/select_contest\?contest_id=([0-9]+)'"
if __name__ == '__main__':
    ses = requests.Session() 
    ses.post(base+'login', data={
        'user_id': credentials.XDOJ_USERNAME,
        'password': credentials.XDOJ_PASSWORD,
        'image.x': random.randint(1, 100),
        'image.y': random.randint(1, 20)
    })
    for cid in re.findall(regex_contest,ses.get(base+'team/list_contest.jsp').text):
        contests.append(cid)

    for t in contests:
        ses.get(base + 'select_contest?contest_id='+str(t))
        res.append(ses.get(base+'team/myruns.jsp?menu=3').text)
    os.mkdir('correct')
    os.mkdir('wrong')
    for groups in res:
        for j in re.findall(regex_filename, groups):
            result = ses.get(base+'getrunsource?run_file='+j[1])
            if j[0] == 'green':
                codefile = open('correct/'+j[1][12:], 'w')
            elif j[0] == 'red':
                codefile = open('wrong/'+j[1][12:], 'w')
            codefile.write(result.text)
            codefile.close()
