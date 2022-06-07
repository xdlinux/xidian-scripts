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
try:
    pkg_resources.require(('requests', 'pyquery'))
except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
    subprocess.check_call([
        sys.executable, '-m', 'pip', 'install', 'requests', 'pyquery'
    ])

import requests as rq
from pyquery import PyQuery as pq

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
root_url = 'https://news.xidian.edu.cn/'
news_dic = []


def req(url):
    #获取页面函数
    response = rq.get(url, headers=headers)
    response.encoding = 'utf-8'
    html = response.text
    doc = pq(html)
    return doc


def extract(doc):
    '''
    提取首页url函数
    doc1是banner头条新闻部分，banner下面有三栏，
    doc2是第一栏工作动态
    doc3是第二栏是全网新闻
    第三栏是热点新闻，调用API方法所以另写函数
    其他页面没啥意思，如果想写的话可以自己写，parse可以通用
    '''

    urls = []

    doc1 = doc('.content1_left')
    doc1('.content1_left_top tbody tr:first-child').remove()
    doc1('.content1_left_bottom_top').remove()
    for url in doc1('a').items():
        urls.append(url.attr.href)

    doc2 = doc('.gzdt_bottom ul')
    for url in doc2('li a:last-child').items():
        urls.append(url.attr.href)

    doc3 = doc('.mtxd_bottom')
    for url in doc3('a').items():
        if(url.attr.href[0] == 'i'):
            urls.append(url.attr.href)

    dic4 = get_hot_news()
    for dic in dic4:
        urls.append(dic['linkurl'])

    return urls


def parse(url):
    #子页面处理函数
    doc = req(root_url + url)
    doc('#wz_zw img').remove()
    doc('#wz_zw span').remove()

    tag = doc('.yaowen-a').text()
    title = doc('.neirong-bt').text()
    date = doc('#date').text()[5:21]  # 发布时间：2020-12-01 08:52:41   自行调整切片
    source = doc('#from').text()
    author = doc('.editor').text()  # 责任编辑：XXX   自行调整切片
    content = doc('#wz_zw p').text()  # 如果需要换行符请手写re，默认段与段直接以空格间隔

    #首个图片的链接
    if doc('.img_vsb_content').attr.src:
        picurl = root_url[0:-1] + doc('.img_vsb_content').attr.src
    else:
        picurl = ''

    news_dic.append(dict(zip(["tag", "title", "date", "author", "content", "picurl"],
                             [tag, title, date, author, content, picurl])))


def get_hot_news():
    #因为这个热点新闻是调用API获取的，所以另写函数
    data = {
        'owner': '1271716923',
        'treeid': '1001',
        'viewid': '189460',
        'mode': '10',
        'locale': 'zh_CN',
        'pageUrl': '%2Findex.htm',
        'uniqueId': 'u38',
        'actionmethod': 'getnewslist'
    }

    json_raw = rq.post(
        'https://news.xidian.edu.cn/system/resource/js/news/hotdynpullnews.jsp', data=data)

    return eval(json_raw.text)


if __name__ == '__main__':
    doc = req(root_url)
    urls = extract(doc)
    #爱护学校服务器，测试请取urls切片
    for url in urls[25:30]:
        parse(url)
    print(news_dic)


'''
输出格式示例
[{
    'tag': '西电要闻',
    'title': '西电举办第五届“三好三有”研究生导学团队评审会',
    'date': '2020-11-30 09:38',
    'author': ' 责任编辑：冯毓璇',
    'content': '西电新闻网讯（通讯员 霍学浩 高宇星）11月27日下午，西安电子科技大学第五届“三好三有”研究 生导学团队评审会在北校区大礼堂举行...',
    'picurl': 'https://news.xidian.edu.cn/__local/F/9A/57/DD2D65A251C04AE5C33ADA469B3_E66B88F8_4CA34.jpg'
}, {
    'tag': '西电要闻',
    'title': '师德标兵｜秦枫：知行合一的“大先生”',
    'date': '2020-12-01 10:26',
    'author': '责任编辑：冯毓璇',
    'content': '  ■学生记者 彭怡乐  宫懿伦 赵晨晋 顾启宇 自1992年任教以来，秦枫已在三尺讲台上辛勤耕耘了28年，她精进自身、知行合一、严谨治学...',
    'picurl': 'https://news.xidian.edu.cn/__local/E/EC/25/D514D9A10754ADA29CCDB064439_93C52D97_7C020.jpg'
}]
'''
