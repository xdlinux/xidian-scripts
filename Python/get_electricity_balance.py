# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 16:16:54 2019

@author: lwz322@qq.com
"""
import os
import time
from selenium import webdriver
from PIL import Image
#import matplotlib.pyplot as plt
import pytesseract
import sys
import configurations, credentials

USERNAME = credentials.ELECTRICITY_USERNAME
PASSWORD = credentials.ELECTRICITY_PASSWORD

if len(sys.path[0])==0:
    cwd=os.getcwd()
else:
    cwd=sys.path[0]

img_path=os.path.join(cwd, "DrawHandler.ashx")

option = webdriver.ChromeOptions()
option.add_argument("--headless")
option.add_argument("--no-sandbox")
option.add_argument('--disable-gpu')
prefs = {'profile.default_content_settings.popups': 1, 'download.default_directory': cwd,"download.prompt_for_download": False}
option.add_experimental_option('prefs', prefs)

def noise_remove_pil(img, k):
    def calculate_noise_count(img_obj, w, h):
        count = 0
        width, height = img_obj.size
        for _w_ in [w - 1, w, w + 1]:
            for _h_ in [h - 1, h, h + 1]:
                if _w_ > width - 1:
                    continue
                if _h_ > height - 1:
                    continue
                if _w_ == w and _h_ == h:
                    continue
                if img_obj.getpixel((_w_, _h_)) < 230:
                    count += 1
        return count
    gray_img = img.convert('L')
    w, h = gray_img.size
    for _w in range(w):
        for _h in range(h):
            if _w == 0 or _h == 0:
                gray_img.putpixel((_w, _h), 255)
                continue
            pixel = gray_img.getpixel((_w, _h))
            if pixel == 255:
                continue
            if calculate_noise_count(gray_img, _w, _h) < k:
                gray_img.putpixel((_w, _h), 255)
    return gray_img

def get_img():
    try:
        driver.get("http://10.168.55.50:8088/searchWeb/DrawHandler.ashx")
    except:
        print("get_img Error")
        clean_quit()
        
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': cwd}}
    driver.execute("send_command", params)

def get_captcha_string():
    string_len=0
    while string_len != 4:
        timeout=5
        while os.path.isfile(img_path) is False:
            get_img()
            time.sleep(1)
            timeout=timeout-1
            if timeout<0:
                print("download timeout")
                clean_quit()
                quit()
        try:
            fp = open(img_path,'rb')
            raw_img = Image.open(fp)
        except:
            print("File read error")
            clean_quit()
            break
        #L_img = raw_img.convert('L')
        ##original L captcha
        #plt.imshow(raw_img)
        #captcha_string = pytesseract.image_to_string(captcha_img, config="--psm 7 DIGITS_CAPS")
        captcha_img = noise_remove_pil(raw_img,4)
        #plt.imshow(captcha_img)
        try:
            captcha_string = pytesseract.image_to_string(captcha_img, config="--psm 7 DIGITS_CAPS")
        except:
            captcha_string = pytesseract.image_to_string(captcha_img, config="--psm 7")
        #print(captcha_string)
        string_len=len(captcha_string)
        fp.close()
        os.remove(img_path)
    return captcha_string

def login():
    driver.get("http://10.168.55.50:8088/searchWeb/Login.aspx")
    driver.find_element_by_id("webName").send_keys(USERNAME)
    driver.find_element_by_id("webPass").send_keys(PASSWORD)
    Success=False
    while not Success:
        captcha_string=get_captcha_string()
        driver.find_element_by_id("txtRandomCode").send_keys(captcha_string)
        try:
            driver.find_element_by_id("Submit1").click()
            driver.get("http://10.168.55.50:8088/searchWeb/webFrm/met.aspx")
            Success=True
        except:
            print('验证码错误，正在重试...')
            try:
                driver.switch_to.alert.accept()
            except:
                print('Alert accept failed')
                clean_quit()
            driver.find_element_by_id("txtRandomCode").clear()
    
    rest = driver.find_element_by_xpath('//*[@id="GV_Info"]/tbody/tr[2]/td[6]').text
    #print("-------------------------------------------------")
    ctime=time.ctime()
    print(ctime,"%s"%rest)

def clean_quit():
    driver.quit()

if __name__ == '__main__':
   if os.path.isfile(img_path):
       os.remove(img_path)
   driver = webdriver.Chrome(options=option)
   login()
   clean_quit()