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
    USERNAME = credentials.SPORTS_USERNAME
    PASSWORD = credentials.SPORTS_PASSWORD
except ImportError:
    USERNAME, PASSWORD = [os.getenv(i) for i in ('SPORTS_USER', 'SPORTS_PASS')]
if not USERNAME or not PASSWORD:
    print('请设置环境变量 SPORTS_USER 和 SPORTS_PASS')
    exit(1)


from libxduauth import SportsSession

def get_current_term(session):
    response = session.post(session.BASE_URL + 'stuTermPunchRecord/findList',
                            data={
                                'userId': session.user_id
                            }).json()
    return (response['data'][0]['sysTermId'], response['data'][0]['sysTerm'])


def get_valid_punch_records(session, term_id):
    response = session.post(session.BASE_URL + 'stuPunchRecord/findPagerOk',
                            data={
                                'userNum': USERNAME,
                                'sysTermId': term_id,
                                'pageSize': 999,
                                'pageIndex': 1
                            }).json()
    return len(response['data'])


def get_all_punch_records(session, term_id):
    response = session.post(session.BASE_URL + 'stuPunchRecord/findPager',
                            data={
                                'userNum': USERNAME,
                                'sysTermId': term_id,
                                'pageSize': 999,
                                'pageIndex': 1
                            }).json()
    return len(response['data'])


if __name__ == '__main__':
    ses = SportsSession(USERNAME, PASSWORD)
    (term_id, term_name) = get_current_term(ses)
    print('当前学期: ' + term_name)
    valid_count = get_valid_punch_records(ses, term_id)
    print('有效打卡次数: ' + str(valid_count))
    all_count = get_all_punch_records(ses, term_id)
    print('总打卡次数: ' + str(all_count))
