# -*- coding: utf-8 -*-
"""
Created on Tue May 30 19:47:22 2017

@author: vini
"""
Host='127.0.0.5'
Port=50127
from socket import socket, AF_INET, SOCK_STREAM
clientsocket = socket(AF_INET,SOCK_STREAM)
clientsocket.connect((Host, Port))
clientsocket.sendall('hello, world')
data=clientsocket.recv(1024)
print ("received", data, "from server", Host)
clientsocket.close()

