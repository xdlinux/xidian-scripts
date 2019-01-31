import auth.wx
import auth.utils
import credentials
from datetime import datetime


if __name__ == '__main__':
    ses = auth.wx.get_login_session(credentials.IDS_USERNAME, credentials.IDS_PASSWORD)
    data = {
        "appKey": "GiITvn",
        "param": "{}",
        "secure": 0
    }
    result = ses.post(auth.wx.BASE + 'infoCampus/playCampus/getAllPurposeCard.do', json=data).json()
    print("一卡通余额: " + str(int(result["allPurposeCardVO"]["cardGeneralInfo"][0]["value"]) / 100) + " 元")
    print("继续查询消费记录请按回车，否则请关闭...")
    input()
    print("查询时间跨度不能超过 30 天。")
    while True:
        start_date = input("请输入开始时间 (格式: 年-月-日): ")
        end_date = input("请输入开始时间 (格式: 年-月-日): ")
        if (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days <= 30:
            data = {
                "appKey": "GiITvn",
                "param": '{{\"startDate\":\"{}\",'
                         '\"endDate\":\"{}\",'
                         '\"offset\":1,'
                         '\"cardNo\":null}}'.format(datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%d"),
                                                    datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%d")),
                "time": auth.utils.timestamp(),
                "secure": 0
            }
            result = ses.post(auth.wx.BASE + 'infoCampus/playCampus/getExpenseRecords.do', json=data).json()
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

