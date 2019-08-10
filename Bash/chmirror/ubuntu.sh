#!/bin/bash

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