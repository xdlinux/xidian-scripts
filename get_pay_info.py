import time
import os
import requests
from lxml import html
from PIL import Image
from io import BytesIO
from auth.GLOBAL import HEADER

USE_TESSERACT = True
USERNAME = "student id"
PASSOWORD = "password"

BASE_URL = "https://pay.xidian.edu.cn"

PAY_INFO_URL = "/home"
LOGIN_URL = "/login"

TMP_DIR = os.path.expanduser("~/.xidian/")
IMG_PATH = os.path.join(TMP_DIR, "img.jpg")
TEXT_PATH = os.path.join(TMP_DIR, "result.txt")


def make_data_and_cookies(r):
    """make the post data(including vcode) and get cookies"""

    vcode = ''
    while len(vcode) is not 4:
        doc = html.document_fromstring(r.get(BASE_URL).text)
        vcode_link = doc.cssselect('form img')[0].get('src')
        vcv = doc.cssselect('input[name="_csrf"]')[0].get('value')
        img_url = BASE_URL + vcode_link
        img = ses.get(img_url)

        if USE_TESSERACT == True:
            # write to the image file
            with open(IMG_PATH, 'w') as f:
                f.write(img.content)

            # using tesseract to get the vcode img value
            os.popen('tesseract %s %s' % (IMG_PATH, TEXT_PATH[:-4]))
            with open(TEXT_PATH) as f:
                vcode = f.read().strip('\n')
        else:
            img = Image.open(BytesIO(img.content)).convert('1')
            img = img.resize((int(img.width*0.5),int(0.4*img.height)))
            pt = img.load()
            for y in range(0, img.height-4):
                for x in range(img.width):
                    print('▩' if pt[x, y] == 255 else ' ', end='')
                print()
            vcode = input('验证码：')

    return {
        "LoginForm[username]": USERNAME,
        "LoginForm[password]": PASSOWORD,
        "LoginForm[verifyCode]": vcode,
        "_csrf": vcv,
        "login-button": ""
    }


def get_info(ses):
    """retrieve the data using the cookies"""
    info_url = BASE_URL + PAY_INFO_URL
    s = ses.get(info_url).text
    doc = html.document_fromstring(s)
    result = doc.cssselect('tr[data-key="14"]')[0]
    
    used = result.cssselect('td[data-col-seq="3"]')[0].text
    rest = result.cssselect('td[data-col-seq="7"]')[0].text
    return used, rest

if __name__ == '__main__':
    if USE_TESSERACT and not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)
    while True:
        ses = requests.session()
        ses.headers = HEADER
        data = make_data_and_cookies(ses)
        ses.post(BASE_URL+LOGIN_URL, data=data).text  # login
        ses.get(BASE_URL)
        try:
            result = get_info(ses)
            break
        except:
            ses.close()
            time.sleep(1)
    print("此月已使用流量 %s , 剩余 %s " % (result))
