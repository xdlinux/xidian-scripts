# Copyright (C) 2019 by the XiDian Open Source Community.
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

import auth.wx
import credentials
from datetime import datetime


if __name__ == '__main__':
    ses = auth.wx.get_login_session(
        credentials.WX_USERNAME, credentials.WX_PASSWORD)
    result = ses.post(
        auth.wx.BASE + 'infoCampus/playCampus/getAllPurposeCard.do',
        param={}
    ).json()
    print("一卡通余额: " + str(int(result["allPurposeCardVO"]
                              ["cardGeneralInfo"][0]["value"]) / 100) + " 元")
    