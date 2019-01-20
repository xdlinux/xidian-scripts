import os

USE_TESSERACT = False
# 是否用tesseract识别验证码，默认为否

TMP_DIR = os.path.expanduser("~/.xidian/")
IMG_PATH = os.path.join(TMP_DIR, "img.jpg")
TEXT_PATH = os.path.join(TMP_DIR, "result.txt")
# tesseract