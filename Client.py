# -*- coding: utf-8 -*-
"""
Created on Tue May 30 19:47:22 2017

@author: vini
"""
from socket import socket, AF_INET, SOCK_DGRAM
s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', 0)) # OS chooses port
print ("using", s.getsockname())
server = ('192.168.0.112', 59633)
s.sendto("estou aqui enviando  coisas", server)
data, addr = s.recvfrom(1024)
print ("received", data, "from server", addr)
s.close()
host: local:host
