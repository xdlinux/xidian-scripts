import time
import os
import pytz
import datetime
import requests

try:
    import credentials
    USERNAME = credentials.IDS_USERNAME
    PASSWORD = credentials.IDS_PASSWORD
except ImportError:
    USERNAME, PASSWORD = [os.getenv(i) for i in ('IDS_USER', 'IDS_PASS')]


def commit_data(username, password):
    sess = requests.session()
    sess.post(
        'https://xxcapp.xidian.edu.cn/uc/wap/login/check', data={
            'username': username,
            'password': password
        })
    return sess.post(
        'https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/save', data={
            'sfzx': '1', 'tw': '1',
            'area': '陕西省 西安市 长安区',
            'city': '西安市', 'province': '陕西省',
            'address': '陕西省西安市长安区兴隆街道梧桐大道西安电子科技大学长安校区',
            'geo_api_info': '{"type":"complete","position":{"Q":34.129092068143,"R":108.83138888888902,"lng":108.831389,"lat":34.129092},"location_type":"html5","message":"Get geolocation success.Convert Success.Get address success.","accuracy":65,"isConverted":true,"status":1,"addressComponent":{"citycode":"029","adcode":"610116","businessAreas":[],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"雷甘路","streetNumber":"266#","country":"中国","province":"陕西省","city":"西安市","district":"长安区","township":"兴隆街道"},"formattedAddress":"陕西省西安市长安区兴隆街道梧桐大道西安电子科技大学长安校区","roads":[],"crosses":[],"pois":[],"info":"SUCCESS"}',
            'sfcyglq': '0', 'sfyzz': '0', 'qtqk': '', 'ymtys': '0'
        }
    ).json()['m']


def send_log(student_id, message):
    if requests.post(
        'http://XduCheckInLog.117503445.top:8013/api/log', json={
            "student_id": str(student_id),
            "message": message
        }
    ).text != 'success':
        print('日志收集异常，请联系github.com/117503445')


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
    message = commit_data(USERNAME, PASSWORD)
    print(message)
    message = get_hour_message() + '检-' + message

    if not os.getenv('DISABLE_STATS'):
        send_log(USERNAME[:9], message)  # 可选,上传日志,帮助开发者优化程序:D


if __name__ == "__main__":
    main_handler(None, None)
