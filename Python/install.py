#!/usr/bin/python3
import os
import shutil
os.system('pip3 install -r requirements.txt &> /dev/null')
userdir = os.path.join(os.path.expanduser('~'), '.xidian_scripts')
try:
    os.mkdir(userdir)
    os.mkdir(os.path.join(userdir, 'config'))
    shutil.copytree('./tessdata', os.path.join(userdir, 'tessdata'))
    shutil.copy(
        os.path.join('lib', 'config', 'captcha.png'),
        os.path.join(userdir, 'config')
    )
except:
    pass

with open(os.path.join(userdir, 'config', 'config.yml'), 'w') as f:
    f.write(
'''# currently not available
USE_TESSERACT: true
# export_timetable
USE_LATEST_SEMESTER: true
SCHOOL_YEAR: 2019
SEMESTER: '2'
''')