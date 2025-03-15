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

# intro: this script only works at school network environment
#        and this is a zero-config script

import requests
import json
from datetime import datetime
import math

def format_bytes(bytes, decimals=2):
    if bytes <= 0:
        return "0 B"
    suffixes = ["B", "KB", "MB", "GB", "TB"]
    i = int(math.log(bytes, 1000))
    return f"{bytes / math.pow(1000, i):.{decimals}f} {suffixes[i]}"

def get_network_info():
    try:
        response = requests.get(
            'https://w.xidian.edu.cn/cgi-bin/rad_user_info',
            params={
                'callback': 'jsonp',
                '_': str(int(datetime.now().timestamp() * 1000)),
            },
            headers={'Accept': 'text/plain'}
        )
        response.raise_for_status()
        jsonString = response.text[6:-1]

        return json.loads(jsonString)

    except Exception as e:
        print(f'Error fetching network info: {e}')
        isLoading = False
        return None, None, isLoading

if __name__ == '__main__':
    res = get_network_info()
    print(f"Network Info: {res['products_name']}", )
    print(f"Usage: {format_bytes(res['sum_bytes'])}", )
