# xidian-scripts
 
[![License: LGPL v3+](https://img.shields.io/badge/License-LGPL%20v3+-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

## 这是什么？

西安电子科技大学校园生活的一些实用小脚本  

## 开始使用

请在运行脚本前设置一些环境变量。Linux下可以写进`~/.*shrc`

|环境变量|用到这个环境变量的脚本|补充说明|
|:-:|:-:|:-:|
|IDS_USER/IDS_PASS|export_timetable<br>get_grades.py<br>get_borrowed_books<br>check_in<br>get_course_data|对应西电统一认证服务的用户名密码|
|WX_USER/WX_PASS|get_borrowed_books<br>get_card_balance<br>query_card_bill|由于此服务与统一认证密码保持一致，若脚本找不到这两个环境变量，则会使用IDS_USER/IDS_PASS|
|PAY_USER/PAY_PASS|get_network_usage|对应zfw.xidian.edu.cn用户名密码，此脚本由于需要识别验证码，需要安装tesseract才能正常运行，且登陆速度可能较慢|
|ENERGY_USER/ENERGY_PASS|get_electricity_balance|对应宿舍电费账户|
|RS_USER/RS_PASS|get_rs_campus_recruitment|睿思校外站|
|SPORTS_USER/SPORTS_PASS|get_sports_punch_records|对应体适能用户名和密码|
|EXP_CS_PASSWORD|choose_cs_exp|计科院系统实验教学中心密码|

---

如果不想设置环境变量或者想一次性配好所有变量，可以通过编辑`credentials.py`完成：

1. 首先复制`credentials.sample.py`为`credentials.py`
2. 开始编辑`credentials.py`即可

注：`credentials.py`需要和你使用的脚本在同一个路径下

### For Example

在命令行直接运行：
`IDS_USER=学号 IDS_PASS=密码 python3 get_grades.py`

或者在`~/.bashrc`（假如你使用的是bash）中加入：
```sh
export IDS_USER=学号
export IDS_PASS=密码
```
重启终端或执行`source ~/.bashrc`后执行：
`python3 get_grades.py`

### Manifest

* get_borrowed_books: 看看你借过哪些书
* get_card_balance: 查询一卡通余额
* get_electricity_balance*: 查询电量余额
* get_grades: 看看你考了多少分
* get_network_usage: 看看你的 10G 流量还有多少
* get_xdoj_outside: 把你在 `acm.xidian.edu.cn` 上交过的代码都扒拉下来
* export_timetable: 把当前学期课表保存为`.ics`格式，以便导入到日历软件中。
* export_physics_experiment.py*: 将当前学期的物理实验保存为`.ics`格式，以便导入到日历软件中。
* query_card_bill: 查询一卡通在指定时间段（30天内）的消费记录
* get_rs_campus_recruitment: 获取睿思论坛上的校园招聘信息
* check_in: 2020 晨午晚检
* get_sports_punch_records: 查询体育打卡次数
* choose_pe_class: 体育课选课
* choose_cs_exp: 计科院实验选课
* get_course_data:获取课程数据如签到次数，签到率等，保存为csv文件

### 备注

1. 标*号的脚本只能在西电内网使用
1. 设置好上面这些环境变量，就可以直接执行脚本了。你可以只保留或只下载自己所需要的脚本。
1. 如果希望将运行结果推送至类似[Server酱](https://sc.ftqq.com)这样的平台，可以参考下面的命令（以get_rs_campus_recruitment为例）

```bash
echo "text=HR_news&desp=`python3 get_rs_campus_recruitment.py --markdown --urlencode`" | \
    curl -d @- https://sc.ftqq.com/{你的SEKEY}.send
```

## 参与贡献

### As a programmer

直接 PR 即可，同时我们欢迎其他自由的语言实现。  
本仓库的目的更多是鼓励大家尝试在 GitHub 上参与程序的编写，请大胆提 Pull Request，不必担心。
仓库的维护者会尽最大可能帮助你熟悉 git workflow。

### As a reviewer

点击右上角的 watch，关注并检验每一次 PR 并对结果作出回复。  
如何检验？使用 GNU diffutils 或你喜欢的工具应用 PR 邮件里的Patch Links。  

### 要求

至少要保证能在 GNU/Linux 或者其他自由的操作系统下能运行。  
只能在专有的操作系统上运行的不会允许（或者即使程序本身是自由的，但是依赖专有库的也不会允许）。

## 友情链接

[电表](https://www.coolapk.com/apk/249065) by @Robotxm  
[oh-my-xdu](https://github.com/zkonge/oh-my-xdu) by @zkonge
