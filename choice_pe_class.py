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

import time
from io import BytesIO
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from requests import Session
from bs4 import BeautifulSoup
from base64 import b64encode

def encrypt(v, k):
    crypt = AES.new(k, AES.MODE_ECB)
    return b64encode(crypt.encrypt(pad(v,8,'pkcs7')))

def process(username, password):
    whatever = Session()
    login_page = whatever.get("https://xdkd.boxkj.com/admin/login").content
    soup = BeautifulSoup(login_page, 'html.parser')
    the_hash = soup.find('input',id="KEY").get('value')
    code = whatever.get("http://xdkd.boxkj.com/code/captcha-image").content
    Image.open(BytesIO(code)).show()
    code = input("验证码输入：")
    to_post = {
            "uname": encrypt(username.encode(), the_hash.encode()),
            "pwd": encrypt(password.encode(), the_hash.encode()),
            "code": code
        }
    print(to_post)
    result = whatever.post(
        "https://xdkd.boxkj.com/admin/login",
        data=to_post
    )
    print(result.json())
    whatever.post("https://xdkd.boxkj.com/admin/loginUser")
    classes = whatever.post("http://xdkd.boxkj.com/admin/chooseCurriculum/showTeachingCurriculum").json()["data"]
    for i in classes:
        print(f'{str(i["id"])} {i["sysUserName"]} {i["teachingCurriculumName"]} {i["teachingSchoolTimeName"]}')
    ohyeah = input("输入你想上课程的id: ")
    choice = whatever.post(f"http://xdkd.boxkj.com/admin/stuTeacherCurriculum/chooseTeachingCurriculum?teaCurriculumid={ohyeah}&_={int(round(time.time() * 1000))}")
    print(choice.content.decode())

if __name__=="__main__":
    username = input("输入帐号：")
    password = input("输入密码：")
    process(username,password)


