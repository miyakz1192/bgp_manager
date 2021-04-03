#!/usr/bin/env python3

from netmiko import Netmiko
from netmiko import ConnectHandler, file_transfer
import re
import os
import copy
import argparse


class VyOS:
    def __init__(self, args, **kwargs):
        self.args = args
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

    def _max_tunnel_device_index(self):
        connection = self.connection_vyos
        output = connection.send_command("python3 ./bgp_manager_agent.py")
        
        max_num=-1
        for dev in output.split():
            if re.match("^tun[0-9]+$", dev):
                dev_num = int(dev[3:])
                if max_num < dev_num:
                    max_num = dev_num
        return max_num

    def _input_yes_or_no(self):
        while True:
            v = input("Enter yes or no:")
            if v == "yes" or v == "no":
                break
        return v


    def create_tunnel_and_bgp(self):
        if self.args.tunnel == "ip6ip6":
            tun = self._create_tunnel_ip6ip6()
        elif self.args.tunnel == "gre":
            tun = self._create_tunnel_gre()
        bgp = self._create_bgp()
        print("configurations")
        for conf in tun + bgp:
            print(conf)

        if self.args.yes_to_all == False:
            if self._input_yes_or_no() == "no":
                print("executing is quitted")
                return
        print("executing commands to VyOS")
        return


    def _create_tunnel_common(self):
        tundev = "tun" + str(self._max_tunnel_device_index() + 1)
        tunnel = self.args.tunnel
        tusip  = self.args.tunnel_underlay_sip 
        tudip  = self.args.tunnel_underlay_dip
        teip   = self.args.tunnel_endpoint_sip
        
        cmds = [ "set interfaces tunnel " + tundev + " encapsulation " + tunnel,
                 "set interfaces tunnel " + tundev + " source-address " + tusip,
                 "set interfaces tunnel " + tundev + " remote " + tudip,
                 "set interfaces tunnel " + tundev + " address " + teip]
        return cmds, tundev

    def _create_tunnel_ip6ip6(self):
        return self._create_tunnel_common()[0]

    def _create_tunnel_gre(self):
        cmds1,tundev = self._create_tunnel_common()
        cmds2 = ["set interfaces tunnel " + tundev + " parameters ip ttl 255"]
        return  cmds1 + cmds2

    def _create_bgp(self):
        my_as = self.args.my_as
        tedip = self.args.tunnel_endpoint_dip
        cmds = [ "set protocols bgp " + my_as + " neighbor " + tedip + " address-family ipv6-unicast",
                 "set protocols bgp " + my_as + " neighbor " + tedip + " remote-as " + self.args.remote_as]
        return cmds

def yes_no_to_True_False(s):
    if s.lower() == "yes":
        return True
    if s.lower() == "no":
        return False


def analyze_option():
    parser = argparse.ArgumentParser(description="args for bgp_manager")
    parser.add_argument('my_as', help="my AS number")
    parser.add_argument('remote_as', help="AS number to connect to")
    parser.add_argument('tunnel', help="tunnel type for ip6ip6 or gre")
    parser.add_argument('tunnel_underlay_sip', help="tunnel underlay address(source)")
    parser.add_argument('tunnel_underlay_dip', help="tunnel underlay address(destination)")
    parser.add_argument('tunnel_endpoint_sip', help="tunnel address(my side)")
    parser.add_argument('tunnel_endpoint_dip', help="tunnel address(remote side)")
    parser.add_argument('--yes_to_all', help="answer yes to all")
    a = parser.parse_args()  

    if a.yes_to_all == None:
        a.yes_to_all = "no"
    a.yes_to_all = yes_no_to_True_False(a.yes_to_all)

    if "/" not in a.tunnel_endpoint_sip:
        print("ERROR: tunnel_endpoint_sip must with prefix")
        exit(1)

    if "/" in a.tunnel_endpoint_dip:
        a.tunnel_endpoint_dip = a.tunnel_endpoint_dip.split("/")[0]

    if not(a.tunnel == "gre" or a.tunnel == "ip6ip6"):
        print("ERROR: tunnel type illegal")
        exit(1)

    return a



def main():
    args = analyze_option()
    kwargs = {"username": os.environ["BGP_MANAGER_DEVICE_USER_NAME"],
              "ip": os.environ["BGP_MANAGER_DEVICE_IP"],
              "password": os.environ["BGP_MANAGER_DEVICE_PASSWD"],
              "key_file":os.environ["BGP_MANAGER_DEVICE_KEY_FILE"]}
    
    vyos = VyOS(args, **kwargs)
    vyos.connect()
    
    vyos.send_agent()
    vyos.create_tunnel_and_bgp()
    
    vyos.disconnect()

if __name__ == "__main__":
    main()
#    test()


