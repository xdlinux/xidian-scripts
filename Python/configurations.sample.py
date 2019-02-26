# Copyright (C) 2019 by the XiDian Open Source Community.
#
# This file is part of xidian-scripts.
#
# xidian-scripts is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# xidian-scripts is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with xidian-scripts.  If not, see <http://www.gnu.org/licenses/>.

import os

USE_TESSERACT = False
# 是否用tesseract识别验证码，默认为否

# tesseract
TMP_DIR = os.path.expanduser("~/.xidian/")
IMG_PATH = os.path.join(TMP_DIR, "img.jpg")
TEXT_PATH = os.path.join(TMP_DIR, "result.txt")

# export_timetable
USE_LATEST_SEMESTER = True  # 自动获取学期学年信息, 若为True, 可以不填写下方配置项
SCHOOL_YEAR = (2018, 2019)  # 学年度
SEMESTER = '2'              # 学期