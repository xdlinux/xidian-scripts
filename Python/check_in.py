import requests
import json
import time
import pytz
import datetime

try:
    import credentials
    USERNAME = credentials.IDS_USERNAME
    PASSWORD = credentials.IDS_PASSWORD
except ImportError:
    import os
    USERNAME, PASSWORD = [os.getenv(i) for i in ('IDS_USER', 'IDS_PASS')]


def login(session, username, password):
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://xxcapp.xidian.edu.cn',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://xxcapp.xidian.edu.cn/uc/wap/login',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    data = {
        'username': username,
        'password': password
    }

    response = session.post(
        'https://xxcapp.xidian.edu.cn/uc/wap/login/check', headers=headers, data=data)
    # print(response.status_code, response.cookies)


def commit(session):
    headers = {
        'Host': 'xxcapp.xidian.edu.cn',
        'Accept': 'application/json, text/plain, */*',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://xxcapp.xidian.edu.cn',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.14(0x17000e27) NetType/WIFI Language/zh_CN',
        'Connection': 'keep-alive',
        'Referer': 'https://xxcapp.xidian.edu.cn/site/ncov/xidiandailyup',
        'Content-Length': '1835',
    }

    data = {
        'sfzx': '1',
        'tw': '1',
        'area': '陕西省 西安市 长安区',
        'city': '西安市',
        'province': '陕西省',
        'address': '陕西省西安市长安区兴隆街道梧桐大道西安电子科技大学长安校区',
        'geo_api_info': '{"type":"complete","position":{"Q":34.129092068143,"R":108.83138888888902,"lng":108.831389,"lat":34.129092},"location_type":"html5","message":"Get geolocation success.Convert Success.Get address success.","accuracy":65,"isConverted":true,"status":1,"addressComponent":{"citycode":"029","adcode":"610116","businessAreas":[],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"雷甘路","streetNumber":"266#","country":"中国","province":"陕西省","city":"西安市","district":"长安区","township":"兴隆街道"},"formattedAddress":"陕西省西安市长安区兴隆街道梧桐大道西安电子科技大学长安校区","roads":[],"crosses":[],"pois":[],"info":"SUCCESS"}',
        'sfcyglq': '0',
        'sfyzz': '0',
        'qtqk': '',
        'ymtys': '0'
    }

    response = session.post('https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/save',
                            headers=headers, data=data)

    # print(response.status_code, response.text)
    return response


def commit_data(username, password):
    sess = requests.session()
    login(sess, username, password)
    res = commit(sess)
    js = json.loads(res.text)
    return js['m']


def server_jiang_push(SCKEY: str, message):
    requests.get(f'https://sc.ftqq.com/{SCKEY}.send?text={message}')


def send_log(student_id, message):
    js = json.dumps({"student_id": str(student_id),
                     "message": message}, ensure_ascii=False).encode('utf-8')

    res = requests.post(
        'http://XduCheckInLog.117503445.top:8013/api/log', data=js)
    if res.text == 'success':
        print('log success')

# return '晨' or '午' or '晚' or '凌晨'


def get_hour_message():
    h = datetime.datetime.fromtimestamp(
        int(time.time()), pytz.timezone('Asia/Shanghai')).hour
    if 6 <= h <= 11:
        return '晨'
    elif 12 <= h <= 17:
        return '午'
    elif 18 <= h <= 24:
        return '晚'
    else:
        return '凌晨'


def main_handler(event, context):

    # https://sc.ftqq.com/3.version
    # 基于 Server 酱的推送服务,
    SCKEY = ''

    message = commit_data(USERNAME, PASSWORD)
    print(message)
    message = get_hour_message() + '检-' + message
    if SCKEY != '':
        server_jiang_push(SCKEY, message)

    send_log(USERNAME, message)  # 可选,上传日志,帮助开发者优化程序:D


if __name__ == "__main__":
    main_handler(None, None)
