#!/usr/bin/env python3

from netmiko import Netmiko
from netmiko import ConnectHandler, file_transfer
import re
import os

user_name=os.environ["BGP_MANAGER_DEVICE_USER_NAME"]
device_type="vyos"
agent_file_name="bgp_manager_agent.py"

remote_device = {'device_type': device_type,
                 'ip': os.environ["BGP_MANAGER_DEVICE_IP"],
                 'username': user_name,
                 'use_keys': True,
                 'password': os.environ["BGP_MANAGER_DEVICE_PASSWD"],
                 'key_file': os.environ["BGP_MANAGER_DEVICE_KEY_FILE"]}

connection = Netmiko(**remote_device)



# コマンド実行
output = connection.send_command('show ipv6 route')
print(output)
print("ls somewhere")
output = connection.send_command('ls /home/vyos')
print(output)
print("getting pwd")
output = connection.send_command('pwd')
print(output)

connection.disconnect()


source_file="bgp_manager_agent.py"
dest_file=source_file
file_system="/home/" + user_name + "/"
direction="put"

print("sending agent to VyOS")
#remote_device["device_type"] = "linux_ssh"
remote_device["device_type"] = "linux"
connection = Netmiko(**remote_device)
transfer_dict = file_transfer(connection,
                              source_file=source_file, 
                              dest_file=dest_file,
                              file_system=file_system, 
                              direction=direction,
                              overwrite_file=True)
print(transfer_dict)
connection.disconnect()

print("getting tunnel interface names")
remote_device["device_type"] = "linux"
connection = Netmiko(**remote_device)
output = connection.send_command("python3 ./bgp_manager_agent.py")

max_num=0
for dev in output.split():
    if re.match("^tun[0-9]+$", dev):
        print(dev)
        dev_num = int(dev[3:])
        print(dev_num)
        if max_num < dev_num:
            max_num = dev_num

print("max_num=" + str(max_num))
        
    

connection.disconnect()
