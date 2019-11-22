# xidian-scripts/Python

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)  
[![License: LGPL v3+](https://img.shields.io/badge/License-LGPL%20v3+-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

## 这是什么？

西安电子科技大学校园生活的一些实用 Python 小脚本

## 开始使用

1. 在此目录(xidian-scripts/Python/)下执行`python3 install.py`
1. 根据`credentials.sample.py`创建并填写`credentials.py`
1. 在任意目录都可执行`python3 <path-to-script>`

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

## 备注

1. 如果你安装了tesseract，脚本理论上能自动启用tesseract进行验证码识别
1. 标*号的脚本只能在西电内网使用

## 关于tesseract的使用

1. tesseract可以用作简单的验证码识别，关于如何安装与使用它，请参考[tesseract](https://github.com/tesseract-ocr/tesseract/wiki)，当然你也可以选择不用它，仅仅安装pytesseract的python库而不安装其本体。(这样脚本才不会由于无法import pytesseract而报错)。
1. @lllthhhh 自行标注了一些来自zfw.xidian.edu.cn的验证码进行了训练。其训练结果ar.traineddata将在执行`python3 install.py`时放置于`~/.xidian_scripts`
