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


try:
    USE_TESSERACT = True
    import os
    import lib.utils as utils
    from PIL import Image
    assert(utils.try_get_vcode(
        Image.open(os.path.join(
            os.path.expanduser('~'), 
            '.xidian_scripts', 'config', 'captcha.png'
        )))[1] == '2238')
except:
    USE_TESSERACT = False

# export_timetable
USE_LATEST_SEMESTER = True  # 自动获取学期学年信息, 若为True, 可以不填写下方配置项
SCHOOL_YEAR = (2018, 2019)  # 学年度
SEMESTER = '2'              # 学期
