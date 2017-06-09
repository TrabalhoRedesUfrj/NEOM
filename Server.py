# -*- coding: utf-8 -*-
"""
Created on Tue May 30 19:42:34 2017
@author: vini
"""
from socket import socket, AF_INET, SOCK_DGRAM
s = socket(AF_INET, SOCK_DGRAM)
s.bind(('192.168.0.105',59633))
print ("using", s.getsockname())
while True:
    (data, addr) = s.recvfrom(1024)
    print ("Connection from", addr)
    print ("estou aqui recebendo dado do client:", data, "from Client", addr)
    data1="Ola estou recebendo sua menssagem"
    s.sendto(data1, addr)
