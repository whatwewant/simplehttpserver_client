# -*- coding: cp936 -*-
import os
import sys
from SimpleHTTPClient import SimpleHTTPClient

ip = ""
port = ""
while ip == "" or port == "":
    ip = raw_input("IP: ")
    ip = ip.strip()
    port = raw_input("�˿�: ")
    port = port.strip()

OO = SimpleHTTPClient(ip, port)
OO.myrun()

raw_input("�������!")
