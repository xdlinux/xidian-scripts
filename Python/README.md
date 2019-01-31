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
* export_timetable: 把当前学期课表保存为iCalendar(.ics)格式，这样就能导入到日历软件中。注意修改第二学期作息更换日期 END_MONTH 和 END_DAY
* get_card_balance: 查询一卡通余额和指定时间段（30天内）的消费记录

## 该怎么用？

1. Python3
1. 一些依赖：requests, lxml, Pillow, icalendar, [tesseract](https://github.com/tesseract-ocr/tesseract/wiki)  
1. 重命名文件： configurations.sample.py -> configurations.py credentials.sample.py -> credentials.py
1. 根据自己需要更改配置文件： configurations.py, credentials.py  
1. 跑起来：python3 [文件名]
