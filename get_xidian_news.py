#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import html
from datetime import datetime, timedelta

# get news in last X days
DAY = 3

# url of the news page
BASE_URL = "http://see.xidian.edu.cn/"

#  get the page content
r = requests.get(BASE_URL)

# override the encoding
r.encoding = 'GBK'

doc = html.document_fromstring(r.text)
today = datetime.today()


def get_today_news():
    trs = doc.cssselect('table[width="98%"] tr')
    for tr in trs:
        img_tag = tr.cssselect('img')
        date_tag = tr.cssselect('font')
        if img_tag and date_tag:
            tr_date = date_tag[0].text_content().strip('[]')
            tr_timedelta = today - datetime.strptime(tr_date, "%Y-%m-%d")
            if tr_timedelta < timedelta(DAY):
                link = tr.cssselect('a')[0].get('href')
                print tr.text_content(), BASE_URL + link

if __name__ == '__main__':
    get_today_news()
