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

import auth.wx
import credentials
from datetime import datetime

if __name__ == '__main__':
    ses = auth.wx.get_login_session(
        credentials.WX_USERNAME, credentials.WX_PASSWORD)
    result = ses.post(
        auth.wx.BASE + 'infoCampus/playCampus/getAllPurposeCard.do',
        param={}
    ).json()

    print("查询时间跨度不能超过 30 天。")
    while True:
        start_date = input("请输入开始时间 (格式: 年-月-日): ")
        end_date = input("请输入结束时间 (格式: 年-月-日): ")
        if (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days <= 30:
            param = '{{\"startDate\":\"{}\",' + \
                '\"endDate\":\"{}\",' + \
                '\"offset\":1,' + \
                '\"cardNo\":null}}'
            param = param.format(datetime.strptime(start_date, "%Y-%m-%d").strftime(
                "%Y-%m-%d"), datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%d"))
            result = ses.post(
                auth.wx.BASE + 'infoCampus/playCampus/getExpenseRecords.do', param=param).json()
            if len(result["expenseList"]) == 0:
                print("指定的时间段内没有消费记录。")
                print()
                print("继续查询请按回车，否则请关闭...")
                input()
                continue
            print("消费日期\t消费地点\t收支类型\t消费金额")
            for i in range(len(result["expenseList"])):
                print(result["expenseList"][i][4]["dataValue"] + "\t" +
                      result["expenseList"][i][3]["dataValue"] + "\t" +
                      result["expenseList"][i][5]["dataValue"] + "\t" +
                      str(int(result["expenseList"][i][2]["dataValue"]) / 100))
            print()
            print("继续查询请按回车，否则请关闭...")
            input()
            continue
        else:
            print("查询时间跨度不能超过 30 天。")
            print()
