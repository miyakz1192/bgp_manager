===============================================================================
開発メモ
===============================================================================


netmikoを使ってvyosのbgp接続運用を簡単にする。

https://uktia.hatenablog.jp/entry/20200802/1596295133

https://lab.m-field.co.jp/2020/04/24/netmiko-basic-manual/


https://pynet.twb-tech.com/blog/automation/netmiko-scp.htm



sudo apt install python3-pip

python3 -m pip install netmiko





how to use

source env_config.sh

cat env_config.sh
export BGP_MANAGER_DEVICE_USER_NAME=xxx
export BGP_MANAGER_DEVICE_IP=xxx
export BGP_MANAGER_DEVICE_KEY_FILE=xxx

and you also  set

export BGP_MANAGER_DEVICE_PASSWD






