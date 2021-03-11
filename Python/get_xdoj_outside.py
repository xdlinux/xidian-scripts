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

# contributed by speroxu

import re
import os
import lib.config as config
import lib.utils as utils
import requests
import credentials
from PIL import Image
from io import BytesIO
import pytesseract

base = 'http://acm.xidian.edu.cn/'
dir_name = credentials.XDOJ_USERNAME + '_xdacm'
os.makedirs(dir_name, exist_ok=True)


def login(sess):
    try:
        login_url = base + 'loginpage.php'
        sess.get(login_url)
        vcode_resp = sess.get(base + 'vcode.php')
        img = Image.open(BytesIO(vcode_resp.content))
        if config.USE_TESSERACT:
            res, vcode = utils.try_get_vcode(img)
        else:
            vcode = utils.prompt_vcode(img)
        if vcode == '':
            raise PermissionError
        if 'Verify Code Wrong!' in sess.post(base + 'login.php', data={
            'user_id': credentials.XDOJ_USERNAME,
            'password': credentials.XDOJ_PASSWORD,
            'vcode': vcode,
            'submit': 'Submit'
        }).text:
            raise PermissionError
        return sess
    except PermissionError:
        return login(sess)


def get_status(sess, top=''):
    url = base + 'status.php?user_id=' + credentials.XDOJ_USERNAME + top
    page = sess.get(url).text

    status_reg = r"<span class='btn.*?'>(.*?)<\/span>.*?submitpage.php\?id=([0-9]+)&sid=([0-9]+)"
    params = re.findall(status_reg, page)
    print(params)

    for param in params:
        get_code(sess, 'submitpage.php?id=%s&sid=%s' % (param[1:]), *param)

    np_reg = r'&top=([0-9]+)&prevtop=([0-9]+)>Next\ Page</a>'
    np = re.search(np_reg, page)
    if np.group(1) != np.group(2):
        get_status(sess, np.expand('&top=\\1&prevtop=\\2'))


def get_code(sess, url, status, problem_id, sid):
    # print(url, status, id, sid)
    code_page = sess.get(base + url).text
    code_re_res = re.search(
        r'<option value=\d selected>(.*?)</option>', code_page, re.S)
    code_type = code_re_res.group(1).strip().lower()
    code_type = 'cpp' if code_type == 'c++' else code_type
    origin_code = re.search(
        r'name="source">(.*?)</textarea>', code_page, re.S).group(1)

    os.makedirs(dir_name + '/' + problem_id, exist_ok=True)
    filename = dir_name + '/' + problem_id + '/' + sid + '.' + code_type
    print(filename)
    with open(filename, 'w') as fp:
        fp.write(origin_code)


if __name__ == '__main__':
    oj_sess = login(requests.Session())
    get_status(oj_sess)
