import os
from libxduauth import IDSSession
from credentials import IDS_USERNAME, IDS_PASSWORD
from bs4 import BeautifulSoup
from typing import List

try:
    import credentials
    USERNAME = credentials.IDS_USERNAME
    PASSWORD = credentials.IDS_PASSWORD
except ImportError:
    USERNAME, PASSWORD = [os.getenv(i) for i in ('IDS_USER', 'IDS_PASS')]
if not USERNAME or not PASSWORD:
    print('请设置环境变量 IDS_USER 和 IDS_PASS')
    exit(1)


LOGIN_URL: str = "https://xdspoc.fanya.chaoxing.com/sso/xdspoc"
COURSE_DATA_URL: str = "http://fycourse.fanya.chaoxing.com/courselist/studyCourseDatashow"

session = IDSSession(LOGIN_URL, IDS_USERNAME, IDS_PASSWORD)


def get_course_info(semesternum: int) -> List[List[str]]:
    html = session.get(COURSE_DATA_URL,
                       params={
                           'semesternum': semesternum,
                       }
                       ).text
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    headers = [header.get_text(strip=True) for header in table.find(  # type:ignore
        'thead').find('tr').find_all('th')]  # type:ignore
    data = []
    data.append(headers)
    for row in table.find('tbody').find_all('tr'):  # type:ignore
        row_data = [cell.get_text(strip=True) for cell in row.find_all('td')]
        data.append(row_data)

    return data


if __name__ == "__main__":
    print("请输入学期数，如2023-2024第一学期：20231，输入0则获取全部学期课程信息")
    while True:
        try:
            semesternum = int(input("学期数："))
            break
        except ValueError:
            print("请输入正确的学期数")
    data = get_course_info(semesternum)
    result = [', '.join(sublist) for sublist in data]
    result = '\n'.join(result)
    with open(f'course_data_{semesternum}.txt', 'w') as f:
        f.write(result)
