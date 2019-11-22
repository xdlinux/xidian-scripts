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

import re
import bs4
import requests
import pytesseract
from PIL import Image
from io import BytesIO
from lib.auth.GLOBAL import HEADER
import lib.config as config
import lib.utils as utils
import credentials

USERNAME = credentials.PAY_USERNAME
PASSOWORD = credentials.PAY_PASSWORD

BASE_URL = "https://zfw.xidian.edu.cn"


def login(r):
    vcode = ''
    while len(vcode) is not 4:
        soup = bs4.BeautifulSoup(r.get(BASE_URL).text, "lxml")
        img_url = BASE_URL + \
            soup.find('img', id='loginform-verifycode-image').get('src')
        vcv = soup.find('input', type='hidden').get('value')
        img = Image.open(BytesIO(ses.get(img_url).content))
        if config.USE_TESSERACT:
            # 使用了自定义的语言数据
            res, vcode = utils.try_get_vcode(img)
        else:
            vcode = utils.prompt_vcode(img)
    try:
        if re.findall(
            r'请修复以下错误<\/p><ul><li>(.*?)<',
            r.post(BASE_URL + '/login', data={
                "LoginForm[username]": USERNAME,
                "LoginForm[password]": PASSOWORD,
                "LoginForm[verifyCode]": vcode,
                "_csrf": vcv,
                "login-button": ""
            }).text
        )[0] == '验证码不正确。':
            login(r)
    except:
        pass


def get_info(ses):
    """retrieve the data using the cookies"""
    info_url = BASE_URL + '/home'
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
    try:
        ses = requests.session()
        ses.headers = HEADER
        login(ses)
        ip_list, used, rest, charged = get_info(ses)
        for ip_info in ip_list:
            print(ip_info)
        print("此月已使用流量 %s , 剩余 %s , 充值剩余 %s" % (used, rest, charged))
    except:
        ses.close()
