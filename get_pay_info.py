#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import requests
from lxml import html

USERNAME = "your student no here"
PASSOWORD = "your password"

BASE_URL = "http://pay.xidian.edu.cn"

FORM_URL = "/servlet/login"
PAY_INFO_URL = "/swyh/dyll.jsp"

TMP_DIR = os.path.expanduser("~/.xidian/")
IMG_PATH = os.path.join(TMP_DIR, "img.jpg")
TEXT_PATH = os.path.join(TMP_DIR, "result.txt")


def make_data_and_cookies():
    """make the post data(including vcode) and get cookies"""

    vcode = ''
    while len(vcode) is not 4:
        r = requests.get(BASE_URL)
        doc = html.document_fromstring(r.text)
        vcode_link = doc.cssselect('form img')[0].get('src')
        vcv = doc.cssselect('input[name="vcv"]')[0].get('value')
        img_url = BASE_URL + vcode_link
        img = requests.get(img_url)

        # write to the image file
        with open(IMG_PATH, 'w') as f:
            f.write(img.content)

        # using tesseract to get the vcode img value
        os.popen('tesseract %s %s' % (IMG_PATH, TEXT_PATH[:-4]))
        with open(TEXT_PATH) as f:
            vcode = f.read().strip('\n')

    data = {
            "account": USERNAME,
            "password": PASSOWORD,
            "vcode": vcode,
            "vcv": vcv
            }
    return data, r.cookies


def submit_form(data, cookies):
    """submit the login form so you're logined in"""
    form_action_url = BASE_URL + FORM_URL
    requests.post(form_action_url, data=data, cookies=cookies)


def get_info(cookies):
    """retrieve the data using the cookies"""
    info_url = BASE_URL + PAY_INFO_URL
    r = requests.get(info_url, cookies=cookies)
    doc = html.document_fromstring(r.text)
    used, rest = doc.cssselect('tr')
    used_gb = float(used.findall('td')[1].text) / 1024
    rest_gb = float(rest.findall('td')[1].text) / 1024
    return used_gb, rest_gb

if __name__ == '__main__':
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)
    while True:
        data, cookies = make_data_and_cookies()
        submit_form(data, cookies)
        time.sleep(1)
        try:
            result = get_info(cookies)
            break
        except:
            time.sleep(1)
    print "此月已使用流量 %.2fGB, 剩余 %.2f GB" % (result)
