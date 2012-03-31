#!/usr/bin/env python

import requests
import hashlib
import re
import time
from lxml import html

BASE_URL = "http://219.245.123.226/xdjwWebNew"

LOGIN_URL = BASE_URL + "/systemAdmin/Login.jsp?command=studentLogin"
POST_URL = BASE_URL + "/Servlet/UsersControl"
GRADES_URL = BASE_URL + "/studentStatus/queryScore/query_person_score.jsp"

STUDENT_NO = "student number here"
PASSWORD = "your password"


def login():
    s = requests.session()
    login_page = s.get(LOGIN_URL)

    m = re.search('var sharedValue = (-?\d+)', login_page.text)
    shared_value = m.group(1)
    password = hash_password(PASSWORD, shared_value)

    data = {
            "uid": STUDENT_NO,
            "password": password,
            'command': "studentLogin"
            }

    s.post(POST_URL, data=data)
    return s


def print_grades(s):
    r = s.get(GRADES_URL)
    doc = html.document_fromstring(r.text)
    trs = doc.cssselect('#t1 tr[class]')
    for tr in trs:
        td = tr.findall('td')
        for i in [2, 6]:
            print td[i].text_content().strip().encode('utf-8'),
        print


def hash_password(password, share_value):
    m = hashlib.md5()
    m.update(password)
    first = m.hexdigest()
    m = hashlib.md5()
    m.update(first + share_value)
    return m.hexdigest()


if __name__ == '__main__':
    s = login()
    print_grades(s)
