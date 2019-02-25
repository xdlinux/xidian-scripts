# xidian-scripts/Python

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)  
[![License: LGPL v3+](https://img.shields.io/badge/License-LGPL%20v3+-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

## 这是什么？

西安电子科技大学校园生活的一些实用 Python 小脚本

## Manifest file

* get_pay_info: 看看你的10G流量还有多少
* get_unreturned_books: 看看你还有哪些书没还
* get_xdoj_log: 把你在202.117.120.31/xdoj上交过的代码都扒拉下来
* get_grades: 看看你考了多少分
* export_timetable: 把当前学期课表保存为iCalendar(.ics)格式，这样就能导入到日历软件中。注意修改第二学期作息更换日期 END_MONTH 和 END_DAY。对于一站式服务大厅数据源，还需要设置学期开始日期 TERM_START_DAY
* get_card_balance: 查询一卡通余额
* query_card_bill: 查询一卡通在指定时间段（30天内）的消费记录

## 该怎么用？

1. 请使用Python3(而不是Python2)
1. 安装依赖：执行`pip install requests lxml Pillow icalendar tesseract`  
1. 重命名文件： configurations.sample.py -> configurations.py credentials.sample.py -> credentials.py
1. 根据自己需要更改配置文件： configurations.py, credentials.py  
1. 跑起来：python3 [文件名]

## 备注

1. 为正常使用脚本，请务必按照credentials.sample.py与configurations.sample.py仔细填写credentials.py与configurations.py。
1. tesseract可以用作简单的验证码识别，关于如何使用它，请参考[tesseract](https://github.com/tesseract-ocr/tesseract/wiki)，当然你也可以选择不用它，仅仅安装tesseract的python库而不安装其本体。(这样脚本才不会由于无法import tesseract而报错)
1. 使用Python2有可能能正常使用大部分的功能，然而在编码的过程中不会考虑能否在Python2上正常运行。再者，python2在2020年1月1日起不再维护，pip也会停止对py2的支持。如果你还在用Python2的话赶紧换到py3吧。
1. get_xdoj_log仅能获取开放的题目的你自己的提交记录。但是如果你对代码进行一点小小的魔改的话，你不仅能获取到自己的所有提交记录，还能把所有人交过的所有代码都爬下来。