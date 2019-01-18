from auth.wx import get_login_session

x = get_login_session('your id', 'your passwd')

print('尚未还的书:')
for i in x.post('http://202.117.121.7:8080/oaCampus/library/getReturn.do', json={
    "appKey": "GiITvn",
    "param": "{\"offset\":1}",
    "secure": 0
}).json()['list']:
    print('《'+i['title']+'》'+'应当在'+i['returnDate']+'之前还')