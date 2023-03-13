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

# @author: https://github.com/akynazh
# @date: 2023-03-09

import asyncio
import aiohttp
import time
import os
from prettytable import PrettyTable
from bs4 import BeautifulSoup

try:
    import credentials
    USERNAME = credentials.IDS_USERNAME
    PASSWORD = credentials.EXP_CS_PASSWORD
except ImportError:
    USERNAME, PASSWORD = [os.getenv(i) for i in ('IDS_USER', 'EXP_PASSWORD')]
if not USERNAME or not PASSWORD:
    print('请设置环境变量 IDS_USER 和 EXP_PASSWORD')
    exit(1)

BASE_URL = 'http://222.25.176.4'
MAX_COROUINES = 5
TIMEOUT = 3
CLASS_NO = '2003%BC%B6'


def DUMMY():
    return time.time() * 1000


async def login(session: aiohttp.ClientSession):
    '''尝试登录

    :param aiohttp.ClientSession session
    :return bool: 登录成功与否
    '''
    resp = await session.post(
        url=f'{BASE_URL}/index.php',
        data={
            'username': USERNAME,
            'userpwd': PASSWORD,
            'user': 'student',
        },
    )
    if resp.status != 200:
        return
    session.cookie_jar.update_cookies(resp.cookies)
    resp = await session.get(url=f'{BASE_URL}/student/default.php')
    if resp.status != 200:
        return
    resp_text = await resp.text()
    if resp_text.find(USERNAME) != -1:
        return True


async def get_exp_info(session: aiohttp.ClientSession) -> dict:
    '''尝试获取实验信息：实验名称 => 实验对应编号 => 教室门牌号列表

    :param aiohttp.ClientSession session
    :return dict: 实验信息
    '''
    exp_info = []

    async def get_crnos_by_exp(name: str, cid: str):
        '''根据实验获取对应教室

        :param str name: 实验名称
        :param str cid: 实验编号
        '''
        if cid == '-1':
            return
        resp = await session.get(
            url=
            f'{BASE_URL}/student/ajax-showClassroom.php?dummy={DUMMY()}&cid={cid}&classno={CLASS_NO}',
        )
        if resp.status == 200:
            resp_text = await resp.text()
            crnos = resp_text.split('#')
            exp_info.append({
                'cid': cid.strip(),
                'name': name.strip(),
                'crnos': crnos
            })
        else:
            exp_info.append({'cid': cid, 'name': name, 'crnos': []})

    resp = await session.get(
        url=
        f'{BASE_URL}/student/showCourses.php?dummy={DUMMY()}&classno={CLASS_NO}',
    )
    if resp.status != 200:
        return
    try:
        soup = BeautifulSoup(await resp.text(), 'lxml')
        options = soup.find(id='paikeFormId').find_all('option')
        tasks = [
            asyncio.ensure_future(
                get_crnos_by_exp(name=op.text, cid=op['value']))
            for op in options
        ]
        for task in asyncio.as_completed(tasks):
            await task
        return exp_info
    except Exception as e:
        print(e)
        return


async def submit_exp_choice(session: aiohttp.ClientSession, crno: str,
                            cid: str):
    '''尝试选实验

    :param aiohttp.ClientSession session
    :param str crno: 实验教室
    :param str cid: 实验编号
    :return bool: 是否成功（或需要修改参数）
    '''
    try:
        url = f'{BASE_URL}/student/ajax-submitXuanke.php?dummy={DUMMY()}&user={USERNAME}&crno={crno}&cid={cid}&classno={CLASS_NO}'
        # a sample: http://222.25.176.4/student/ajax-submitXuanke.php?dummy=1678160826939&user=20009100359&crno=E-II312&cid=115&classno=2003%BC%B6
        print(f'开始提交选择，请求地址：{url}')
        resp = await session.get(url=url)
        if resp.status == 200:
            code = await resp.text()
            code = code.strip()
            if code == '1':
                print('选课成功, 你可以在"查看已选课程"查看该课程信息')
                return True
            elif code == '2':
                print('你已经选过此课程了')
                return True
            elif code == '3':
                print('已经被选满')
                return True
            elif code == '4':
                print('提交过程出现错误')
            elif code == '5':
                print('在选择第 1 课次前，不能选择后面的课次')
                return True
            elif code == '6':
                print('你怎么可能点了不是第 1 次课的课程呢')
                return True
            elif code == '-1':
                print('该课程安排已经过了选课日期')
                return True
            else:
                print('出现错误，选课失败')
        else:
            print('出现错误，选课失败')
    except asyncio.CancelledError:
        pass


async def get_submit_res(session):
    '''获取实验选择结果
    '''
    table = PrettyTable()
    url = f'{BASE_URL}/student/showMyCourses.php'
    print('尝试获取实验选择结果......')
    resp = await session.get(url)
    if resp.status == 200:
        try:
            soup = BeautifulSoup(await resp.text(), 'lxml')
            rows = soup.find('table').find_all('tr')
            for i, row in enumerate(rows):
                if i == 0:
                    cols = row.find_all('th')
                    table.field_names = [col.text.strip() for col in cols]
                else:
                    cols = row.find_all('td')
                    table.add_row([col.text.strip() for col in cols])
            print(table)
        except Exception as e:
            print(f'获取失败：{e}')
    else:
        print('获取失败，请重试')


async def main():
    async with aiohttp.ClientSession() as session:
        print('尝试登录......')
        while True:
            if await login(session):
                print('登录成功！')
                break
            print('登录失败，请检查网络或用户名和密码')
            time.sleep(0.5)
        print(f'开启 {MAX_COROUINES} 个协程，尝试获取实验信息......')
        while True:
            info_flag = False
            tasks = [
                asyncio.ensure_future(get_exp_info(session))
                for i in range(MAX_COROUINES)
            ]
            for task in asyncio.as_completed(tasks):
                exp_info = await task
                if exp_info:
                    info_flag = True
                    break
            if info_flag:
                break
        print('成功获取实验信息：')
        for exp in exp_info:
            print(f'实验名称：{exp["name"]}，实验编号：{exp["cid"]}，实验教室：{exp["crnos"]}')
        # choose
        cid = input('请输入实验编号 >>> ')
        crno = input('请输入实验教室 >>> ')
        print(f'开启 {MAX_COROUINES} 个协程，尝试提交选择......')
        # submit choice
        while True:
            submit_flag = False
            tasks = [
                asyncio.create_task(
                    submit_exp_choice(session=session, crno=crno, cid=cid))
                for _ in range(MAX_COROUINES)
            ]
            done, pending = await asyncio.wait(
                tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                if task.result():
                    submit_flag = True
                    for task in pending:
                        task.cancel()
            if submit_flag:
                break
        await get_submit_res(session)


if __name__ == '__main__':
    asyncio.run(main())