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
from auth.GLOBAL import HEADER
import configurations, credentials

USERNAME = credentials.PAY_USERNAME
PASSOWORD = credentials.PAY_PASSWORD

BASE_URL = "https://zfw.xidian.edu.cn"

PAY_INFO_URL = "/home"
LOGIN_URL = "/login"


def make_data_and_cookies(r):
    vcode = ''
    while len(vcode) is not 4:
        soup = bs4.BeautifulSoup(r.get(BASE_URL).text, "lxml")
        img_url = BASE_URL + soup.find('img', id='loginform-verifycode-image').get('src')
        vcv = soup.find('input', type='hidden').get('value')
        img = Image.open(BytesIO(ses.get(img_url).content))
        if configurations.USE_TESSERACT:
            try:
                # 使用了自定义的语言数据
                vcode = pytesseract.image_to_string(img, lang='ar', config="--psm 7 digits")
            except:
                # 针对没有添加自定义的训练数据的情况
                vcode = pytesseract.image_to_string(img, config="--psm 7 digits")
            print(vcode)
        else:
            img = img.convert('1')
            img = img.resize((int(img.width * 0.5), int(0.4 * img.height)))
            pt = img.load()
            for y in range(0, img.height - 4):
                for x in range(img.width):
                    print('*' if pt[x, y] == 255 else ' ', end='')
                print()
            vcode = input('验证码：')
    return {
        "LoginForm[username]": USERNAME,
        "LoginForm[password]": PASSOWORD,
        "LoginForm[verifyCode]": vcode,
        "_csrf": vcv,
        "login-button": ""
    }


def get_info(ses):
    """retrieve the data using the cookies"""
    info_url = BASE_URL + PAY_INFO_URL
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
    while True:
        ses = requests.session()
        ses.headers = HEADER
        data = make_data_and_cookies(ses)
        ses.post(BASE_URL + LOGIN_URL, data=data)  # login
        ses.get(BASE_URL)
        try:
            ip_list, used, rest, charged = get_info(ses)
            break
        except:
            ses.close()
    for ip_info in ip_list:
        print(ip_info)
    print("此月已使用流量 %s , 剩余 %s , 充值剩余 %s" % (used, rest, charged))
