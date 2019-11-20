try:
    import pytesseract
except:
    pass
import lib.config as config
import os


def try_get_vcode(img):
    if not config.USE_TESSERACT:
        return False, ''
    img = img.convert('L')
    try:
        vcode = pytesseract.image_to_string(
            img, lang='ar',
            config="--psm 7 digits --tessdata-dir " +
            os.path.join(os.path.expanduser('~'),
                         '.xidian_scripts', 'tessdata')
        )
    except:
        vcode = pytesseract.image_to_string(
            img, lang='eng', config="--psm 7 digits")
    return True, vcode


def prompt_vcode(img):
    img = img.convert('L')
    img = img.resize((40, 10))

    pixels = img.getdata()
    chars = ["B", "&", "*", ".", " "]
    new_pixels = [chars[pixel//52] for pixel in pixels]
    new_pixels = ''.join(new_pixels)
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + 40]
                   for index in range(0, new_pixels_count, 40)]
    print(*ascii_image, sep='\n')
    return input('验证码：')
