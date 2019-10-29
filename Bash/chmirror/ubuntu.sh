#!/bin/bash
# Copyright (C) 2019 by the XiDian Open Source Community
# 
# xidian-scripts is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# xidian-scripts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with xidian-scripts. If not, see <http://www.gnu.org/licenses/>.

mirror_site="https://linux.xidian.edu.cn/mirrors/ubuntu/"
alternative="https://mirrors.tuna.tsinghua.edu.cn/ubuntu/"

function get_mirror() {
    status=`curl -I -m 10 -o /dev/null -s -w %{http_code} $mirror_site`
    if [ $status -ne '200' ];then
        echo $alternative
    else
        echo $mirror_site
    fi
}

to_use=`get_mirror`
sudo sed -i "s/archive.ubuntu.com/$to_use/g" /etc/apt/sources.list
# apt update