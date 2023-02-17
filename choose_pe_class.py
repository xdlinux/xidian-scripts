# Copyright (C) 2022 by the XiDian Open Source Community.
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

import pkg_resources
import subprocess
import sys
import os
try:
    pkg_resources.require(('libxduauth'))
except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
    subprocess.check_call([
        sys.executable, '-m', 'pip', 'install', 'libxduauth'
    ])

try:
    import credentials
    USERNAME = credentials.IDS_USERNAME
    PASSWORD = credentials.IDS_PASSWORD
except ImportError:
    USERNAME, PASSWORD = [os.getenv(i) for i in ('IDS_USER', 'IDS_PASS')]
if not USERNAME or not PASSWORD:
    print('请设置环境变量 IDS_USER 和 IDS_PASS')
    exit(1)

import time
from libxduauth import IDSSession


def process():
    whatever = IDSSession("http://tybjxgl.xidian.edu.cn", USERNAME, PASSWORD)
    classes = whatever.post(
        "http://tybjxgl.xidian.edu.cn/admin/"
        "chooseCurriculum/showTeachingCurriculum"
    ).json()["data"]
    for i in classes:
        print(
            f'{str(i["id"])} {i["sysUserName"]} '
            f'{i["teachingCurriculumName"]} {i["teachingSchoolTimeName"]}'
        )
    ohyeah = input("输入你想上课程的id: ")
    choice = whatever.post(
        "http://tybjxgl.xidian.edu.cn/admin//"
        "stuTeacherCurriculum/chooseTeachingCurriculum?"
        f"teaCurriculumid={ohyeah}&_={int(round(time.time() * 1000))}"
    )
    print(choice.content.decode())


if __name__ == "__main__":
    process()
