# xidian-scripts/Python

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)  
[![License: LGPL v3+](https://img.shields.io/badge/License-LGPL%20v3+-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

## 这是什么？

西安电子科技大学校园生活的一些实用 Python 小脚本

## 开始使用

1. 如果你之前填写过`credentials.py`，那么就可以直接运行相应的脚本了
1. 否则，请在运行脚本前设置一些环境变量。Linux下可以写进`~/.*shrc`

|环境变量|用到这个环境变量的脚本|补充说明|
|:-:|:-:|:-:|
|IDS_USER/IDS_PASS|export_timetable<br>get_grades.py<br>get_borrowed_books|对应西电统一认证服务的用户名密码|
|WX_USER/WX_PASS|get_borrowed_books<br>get_card_balance<br>query_card_bill|由于此服务与统一认证密码保持一致，若脚本找不到这两个环境变量，则会使用IDS_USER/IDS_PASS|
|PAY_USER/PAY_PASS|get_network_usage|对应zfw.xidian.edu.cn用户名密码，此脚本由于需要识别验证码，需要安装tesseract才能正常运行，且登陆速度可能较慢|
|ENERGY_USER/ENERGY_PASS|get_electricity_balance|对应宿舍电费账户|
|RS_USER/RS_PASS|get_rs_campus_recruitment|睿思校外站|


## For Example

在命令行直接运行：
`IDS_USER=学号 IDS_PASS=密码 python3 get_grades.py`

或者在`~/.bashrc`（假如你使用的是bash）中加入：
```sh
export IDS_USER=学号
export IDS_PASS=密码
```
重启终端或执行`source ~/.bashrc`后执行：
`python3 get_grades.py`

## Manifest file

* get_borrowed_books: 看看你借过哪些书
* get_card_balance: 查询一卡通余额
* get_electricity_balance*: 查询电量余额
* get_grades: 看看你考了多少分
* get_network_usage: 看看你的 10G 流量还有多少
* get_xdoj_outside: 把你在 `acm.xidian.edu.cn` 上交过的代码都扒拉下来
* export_timetable: 把当前学期课表保存为`.ics`格式，以便导入到日历软件中。
* export_physics_experiment.py*: 将当前学期的物理实验保存为`.ics`格式，以便导入到日历软件中。
* query_card_bill: 查询一卡通在指定时间段（30天内）的消费记录
* get_rs_campus_recruitment: 获取睿思论坛伤的校园招聘信息

## 备注

1. 标*号的脚本只能在西电内网使用
1. 设置好上面这些环境变量，就可以直接执行脚本了。你可以只保留或只下载自己所需要的脚本。
1. 如果希望将运行结果推送至类似[Server酱](https://sc.ftqq.com)这样的平台，可以参考下面的命令（以get_rs_campus_recruitment为例）

```bash
echo "text=HR_news&desp=`python3 get_rs_campus_recruitment.py --markdown --urlencode`" | \
    curl -d @- https://sc.ftqq.com/{你的SEKEY}.send
```

## 关于tesseract的使用

1. tesseract可以用作简单的验证码识别，关于如何安装与使用它，请参考[tesseract](https://github.com/tesseract-ocr/tesseract/wiki)，当然你也可以选择不用它，仅仅安装pytesseract的python库而不安装其本体。(这样脚本才不会由于无法import pytesseract而报错)。
1. @lllthhhh 自行标注了一些来自zfw.xidian.edu.cn的验证码进行了训练。zfw的登陆使用了此数据集。
