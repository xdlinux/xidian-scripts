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

m='https://linux.xidian.edu.cn/mirrors/homebrew/brew.git'
a='https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git'

cwd=`pwd`
cd "$(brew --repo)"
git remote set-url origin `if git ls-remote $m >/dev/null 2>&1;then echo $m;else echo $a;fi`
cd $cwd

m='https://linux.xidian.edu.cn/mirrors/homebrew-bottles/'
a='https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles'
status=`curl -I -m 10 -o /dev/null -s -w %{http_code} $m`
if [ $status -ne '200' ];then
    export HOMEBREW_BOTTLE_DOMAIN=$a
else
    export HOMEBREW_BOTTLE_DOMAIN=$m
fi