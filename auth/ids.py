import requests
import re

from auth.GLOBAL import *

REGEX_HIDDEN_TAG = '<input type="hidden" name="(.*)" value="(.*)"'
REGEX_HTML_COMMENT = r'<!--\s*([\s\S]*?)\s*-->'

def get_login_session(target, username, password):
    ses = requests.session()
    ses.headers = HEADER
    page = ses.get(
        'http://ids.xidian.edu.cn/authserver/login',
        params={'service': target}
    ).text
    page = re.sub(REGEX_HTML_COMMENT,'',page)
    params = {i[0]: i[1] for i in re.findall(REGEX_HIDDEN_TAG, page)}
    ses.post(
        'http://ids.xidian.edu.cn/authserver/login',
        params={'service': target},
        data=dict(params,**{
            'username': username,
            'password': password
        })
    )
    return ses

