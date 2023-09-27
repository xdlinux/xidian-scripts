import argparse
import os
from typing import List

from bs4 import BeautifulSoup
from libxduauth import IDSSession

try:
    from credentials import IDS_PASSWORD, IDS_USERNAME
except ImportError:
    IDS_USERNAME, IDS_PASSWORD = [os.getenv(i) for i in ('IDS_USER', 'IDS_PASS')]
if not IDS_USERNAME or not IDS_PASSWORD:
    print('请设置环境变量 IDS_USER 和 IDS_PASS')
    exit(1)


LOGIN_URL: str = "https://xdspoc.fanya.chaoxing.com/sso/xdspoc"
COURSE_DATA_URL: str = "http://fycourse.fanya.chaoxing.com/courselist/studyCourseDatashow"

session = IDSSession(LOGIN_URL, IDS_USERNAME, IDS_PASSWORD)


def get_course_info(semesternum: int) -> List[List[str]]:
    html = session.get(COURSE_DATA_URL, params={
        'semesternum': semesternum,
    }).text
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table')
    headers = [
        header.get_text(strip=True) for header in
        table.find('thead').find('tr').find_all('th')
    ]
    data = [headers]
    for row in table.find('tbody').find_all('tr'):
        row_data = [cell.get_text(strip=True) for cell in row.find_all('td')]
        data.append(row_data)

    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("semesternum", nargs='?', type=int, default=0)
    args = parser.parse_args()
    data = get_course_info(args.semesternum)
    result = [', '.join(sublist) for sublist in data]
    result = '\n'.join(result)
    with open(f'course_data_{args.semesternum}.csv', 'w') as f:
        f.write(result)
    print(f"已将课程数据保存至course_data_{args.semesternum}.csv")
