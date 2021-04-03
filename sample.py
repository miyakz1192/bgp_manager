#!/usr/bin/env python3

from netmiko import Netmiko
from netmiko import ConnectHandler, file_transfer
import re
import os
import copy


class VyOS:
    def __init__(self, **kwargs):
        self.username = kwargs["username"]
        common = copy.copy(kwargs)
        common["use_keys"] = True

        self.remote_device_vyos = copy.copy(common)
        self.remote_device_vyos["device_type"] = "vyos"

        self.remote_device_scp = copy.copy(common)
        self.remote_device_scp["device_type"] = "linux"

        self.agent_file_name="bgp_manager_agent.py"


    def connect(self):
        self.connection_vyos = Netmiko(**self.remote_device_vyos)
        self.connection_scp  = Netmiko(**self.remote_device_scp)

    def disconnect(self):
        self.connection_vyos.disconnect()
        self.connection_scp.disconnect()

    def send_agent(self):
        source_file=self.agent_file_name
        dest_file=source_file
        file_system="/home/" + self.username + "/"
        direction="put"
        file_transfer(self.connection_scp,
                      source_file=source_file, 
                      dest_file=dest_file,
                      file_system=file_system, 
                      direction=direction,
                      overwrite_file=True)

    def max_tunnel_device_index(self):
        connection = self.connection_vyos
        output = connection.send_command("python3 ./bgp_manager_agent.py")
        
        max_num=-1
        for dev in output.split():
            if re.match("^tun[0-9]+$", dev):
                dev_num = int(dev[3:])
                if max_num < dev_num:
                    max_num = dev_num
        return max_num

def main():
    kwargs = {"username": os.environ["BGP_MANAGER_DEVICE_USER_NAME"],
              "ip": os.environ["BGP_MANAGER_DEVICE_IP"],
              "password": os.environ["BGP_MANAGER_DEVICE_PASSWD"],
              "key_file":os.environ["BGP_MANAGER_DEVICE_KEY_FILE"]}
    
    vyos = VyOS(**kwargs)
    vyos.connect()
    
    vyos.send_agent()
    
    print("getting tunnel interface names")
    max_num = vyos.max_tunnel_device_index()
    print("max_index = " + str(max_num))
    
    vyos.disconnect()

if __name__ == "__main__":
    main()
#    test()


