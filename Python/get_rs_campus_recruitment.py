# Copyright (C) 2020 by the XiDian Open Source Community.
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

# python3，需要requests和BeautifulSoup4
import time
import requests
from bs4 import BeautifulSoup


def post():
    # 外网睿思rsbbs
    url = "http://rsbbs.xidian.edu.cn:80/forum.php?mod=forumdisplay&fid=554&filter=typeid&typeid=43"
    payload = ""
    # 需要自己的登陆Cookie，并替换Cookie
    headers = {
        "Cookie": "UM_distinctid=1701ace5355639607b0f-1aeaa0-1701ace5356c6e; Q8qA_2132_nofavfid=1; Q8qA_2132_smile=13D1; Q8qA_2132_saltkey=r8DbaPY; Q8qA_2132_lastvisit=1589028; Q8qA_2132_seccode=933.d2fe089909e; Q8qA_2132_auth=0831yrg7m%2B1FJB%2F2HNTcPnTYAvVBiRJg02E5ZHmCX%2BSgFhDsvU53grA; Q8qA_2132_lastcheckfeed=31579009; Q8qA_2132_home_diymode=1; Q8qA_2132_sid=pj6C; Q8qA_2132_lip=10.170.42.21810; Q8qA_2132_mobile=no; Q8qA_2132_ulastactivity=9dc3o%2Fg8m%2B3yru2FOecXFT%2Fvp9xGrVy9%2FpSf; Q8qA_2132_st_p=315794%7C17Cc217fb2f98a76460d; Q8qA_2132_viewid=tid_50914; Q8qA_2132_sendmail=1; Q8qA_2132_visitedfid=554D565D548D555D217; Q8qA_2132_st_t=315794%7C1650%7Ca287bf604d44db3f3ef2b081d30f6da4; Q8qA_2132_forum_lastvisit=D_554_159650; Q8qA_2132_checkpm=1; Q8qA_2132_lastact=1550%09misc.php%09patch",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        "Referer": "http://rsbbs.xidian.edu.cn/forum.php?mod=forumdisplay&fid=554",
        "Connection": "close",
        "Host": "rsbbs.xidian.edu.cn",
        "Pragma": "no-cache",
        "Accept-Encoding": "gzip, deflate",
        "Cache-Control": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "Accept-Language": "zh,zh-CN;q=0.9,en;q=0.8"
    }
    response = requests.request("GET", url, data=payload, headers=headers)
    # print(response.text)
    html = BeautifulSoup(response.text, 'html.parser')
    info_all = {}
    hr_index = 1
    for link in html.find_all('a'):
        if "atarget" in str(link.get("onclick")):
            # print(link)
            info_link = link.get("href")
            # del 就业招聘版版规
            if "921702" in info_link:
                continue
            # 外网睿思，可直接在微信推送中查看
            info_link = "http://rsbbs.xidian.edu.cn/" + info_link
            # print(info_link)
            info_text = link.get_text(strip=True)
            # print(info_text)
            info_all[info_text] = info_link
            if hr_index == 1:
                first_hr = info_text
            hr_index += 1
    # print(info_all)
    return hr_index, info_all


def push(info_all):
    # Server酱微信推送，需要在http://sc.ftqq.com绑定微信，获取SEKEY，并替换
    url = "https://sc.ftqq.com/SCU89912Tfcd060da0969e0fe995e708f4a70230.send"
    desp_data = ""
    # 推送格式可自定义
    for k, v in info_all.items():
        desp_data += k + ":\t" + v + "\n"
    # print(desp_data)
    req_data = {"text": "rs", "desp": desp_data}
    req_rst = requests.post(url, data=req_data)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " ---> ", req_rst.text)


if __name__ == '__main__':
    # 直接后台运行，使用sleep延时
    # 推荐去掉while循环，使用crontab定时任务来定时执行
    first_hr_new = ""
    while True:
        first_hr, info_all = post()
        if first_hr_new == first_hr:
            continue
        else:
            push(info_all)
        # sleep 2h
        time.sleep(2 * 60 * 60)
