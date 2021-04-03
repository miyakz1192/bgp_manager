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


set protocols bgp 64689 neighbor 2001:470:24:319:0:1::2 address-family ipv6-unicast
set protocols bgp 64689 neighbor 2001:470:24:319:0:1::2 remote-as 4294966449
Enter yes or no:yes
executing commands to VyOS
show ipv6 route

Traceback (most recent call last):
  File "./bgp_manager.py", line 176, in <module>
    main()
  File "./bgp_manager.py", line 172, in main
    vyos.create_tunnel_and_bgp()
  File "./bgp_manager.py", line 89, in create_tunnel_and_bgp
    output = self.connection_vyos.send_command("conf")
  File "/home/a/.local/lib/python3.8/site-packages/netmiko/utilities.py", line 430, in wrapper_decorator
    return func(self, *args, **kwargs)
  File "/home/a/.local/lib/python3.8/site-packages/netmiko/base_connection.py", line 1529, in send_command
    raise IOError(
OSError: Search pattern never detected in send_command: vyos@vyos:\~\$
a@bgpmanager:~/bgp_manager$ 




