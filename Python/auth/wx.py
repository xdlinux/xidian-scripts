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

# wx.xidian.edu.cn
# 能交网费,查成绩,看新闻等等
import requests
import typing
import hashlib
import time
import auth.utils
import random

from auth.GLOBAL import *

BASE = 'http://202.117.121.7:8080/'

class Session: # 封装requests.Session
    _ses: requests.Session

    @property
    def headers(self):
        return self._ses.headers

    @headers.setter
    def headers(self, headers):
        self._ses.headers = headers

    def _dump_sign(self, data: typing.Dict):
        l = list(data.keys())
        l.sort()
        s = ''
        for i in l:
            s += i+'='+str(data[i])+'&'
        s = s[:-1]
        return hashlib.md5(s.encode('utf-8')).hexdigest()
    
    def options(self, url):
        return self._ses.options(url, headers={
            'Access-Control-Request-Headers': 'content-type,token',
            'Access-Control-Request-Method': 'POST'
        })

    def post(self, url, data=None, json=None, headers=None, param=None):
        self.options(url)
        if param is not None:
            json = {
                'appKey': "GiITvn",
                'param': param,
                'secure': 0
            }
        if json is not None:
            json['time']=auth.utils.timestamp() # 先后顺序
            json['sign'] = self._dump_sign(json)  # 数据签名在生成时间戳之后
            if headers == None:
                headers = {}
            headers = dict(headers, **{
                'Content-Type': 'application/json;charset=UTF-8'
            })
        return self._ses.post(url, json=json, data=data, headers=headers)
        

    def __init__(self):
        self._ses = requests.session()
        self._ses.headers = HEADER
        self._ses.headers['token'] = ''

def _generate_uuid():
    a = [str(random.random())[2:10] for i in range(2)]
    a = [a[i]+str(auth.utils.timestamp())[-10:] for i in range(2)]
    a = [hex(int(a[i]))[2:10] for i in range(2)]
    return "web"+a[0]+a[1]


def get_login_session(username, password) -> Session:
    ses = Session()
    data = {
        'appKey': "GiITvn",
        'param': "{{\"userName\":\"{}\","
                 "\"password\":\"{}\","
                 "\"schoolId\":190,"
                 "\"uuId\":\"{}\"}}"
                 .format(username, password, _generate_uuid()),
        'secure': 0
    }
    result = ses.post(BASE+'baseCampus/login/login.do', json=data).json()
    if result['isConfirm'] != 1:
        raise Exception('登录失败') # 请检查credentials.py
    ses.headers['token'] = result['token'][0]+'_'+result['token'][1]
    return ses

