import auth.ids
import json
import credentials


ses = auth.ids.get_login_session(
    'http://ehall.xidian.edu.cn:80//appShow', credentials.IDS_USERNAME, credentials.IDS_PASSWORD)

ses.get('http://ehall.xidian.edu.cn//appShow?appId=4768574631264620', headers={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
})

querySetting = [
    {  # 学期
        'name': 'XNXQDM',
        'value': '2017-2018-2,2018-2019-1',
        'linkOpt': 'and',
        'builder': 'm_value_equal'
    }, {  # 是否有效
        'name': 'SFYX',
        'value': '1',
        'linkOpt': 'and',
        'builder': 'm_value_equal'
    }
]
courses = {}

for i in ses.post(
    'http://ehall.xidian.edu.cn/jwapp/sys/cjcx/modules/cjcx/xscjcx.do',
    data={
        'querySetting=': json.dumps(querySetting),
        '*order': 'KCH,KXH',# 按课程名，课程号排序
        'pageSize': 1000, # 有多少整多少.jpg
        'pageNumber': 1
    }
).json()['datas']['xscjcx']['rows']:
    if i['XNXQDM_DISPLAY'] not in courses.keys():
        courses[i['XNXQDM_DISPLAY']] = []
    courses[i['XNXQDM_DISPLAY']].append((i['XSKCM'].strip(),str(i['ZCJ'])))

for i in courses.keys():
    print(i+':')
    for j in courses[i]:
        print('\t'+j[0]+':'+j[1])