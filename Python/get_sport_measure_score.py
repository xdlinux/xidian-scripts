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
#

from libxduauth import SportsSession
# For a nice output.
from prettytable import PrettyTable

try:
    import credentials
    USERNAME = credentials.SPORTS_USERNAME
    PASSWORD = credentials.SPORTS_PASSWORD
except ImportError:
    import os
    USERNAME, PASSWORD = [os.getenv(i) for i in (
        'SPORTS_USERNAME', 'SPORTS_PASSWORD')]


def get_sport_measure_detail(session, meaScoreId):
    form = PrettyTable()
    form.field_names = ["项目", "结果", "单位", "分数"]
    response = session.post(session.BASE_URL + 'measure/getStuScoreDetail',
                            data={
                                "meaScoreId": meaScoreId
                            }).json()
    for each in response['data']:
        if 'actualScore' in each:
            form.add_row([each["examName"], each["actualScore"],
                         each["examunit"], each["score"]])
        else:
            form.add_row([each["examName"], "未录入", each["examunit"], "未录入"])
    print(form)


def get_sport_measure_general(session):
    response = session.post(session.BASE_URL + 'measure/getStuTotalScore',
                            data={
                                "userId": session.user_id
                            }).json()
    for i in response['data']:
        if 'meaScoreId' in i:
            print("{} 年度的成绩是 {} ，等级是{}。详情如下：".format(
                i['year'], i['totalScore'], i['rank']))
            get_sport_measure_detail(session, i["meaScoreId"])
        else:
            print("目前四次体测成绩总分是 {}".format(i['totalScore']))


if __name__ == '__main__':
    ses = SportsSession(USERNAME, PASSWORD)
    get_sport_measure_general(ses)
