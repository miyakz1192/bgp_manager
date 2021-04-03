#!/usr/bin/env python3

import sys
args = sys.argv
import netifaces as ni
import ipaddress

for iface in ni.interfaces():
  print(iface)

