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
import re

from auth.GLOBAL import *

REGEX_HIDDEN_TAG = '<input type="hidden" name="(.*)" value="(.*)"'
REGEX_HTML_COMMENT = r'<!--\s*([\s\S]*?)\s*-->'

def get_login_session(target, username, password):
    ses = requests.session()
    ses.headers = HEADER
    page = ses.get(
        'http://ids.xidian.edu.cn/authserver/login',
        params={'service': target}
    ).text
    page = re.sub(REGEX_HTML_COMMENT,'',page)
    params = {i[0]: i[1] for i in re.findall(REGEX_HIDDEN_TAG, page)}
    ses.post(
        'http://ids.xidian.edu.cn/authserver/login',
        params={'service': target},
        data=dict(params,**{
            'username': username,
            'password': password
        })
    )
    return ses

