# -*- coding: utf-8 -*-
"""
Created on Tue May 30 19:47:22 2017

@author: vini
"""
Host='127.0.0.5'
Port=50128
from socket import socket, AF_INET, SOCK_STREAM
import ssl,pprint
clientsocket = socket(AF_INET,SOCK_STREAM)
ssl_sock=ssl.wrap_socket(clientsocket,ca_certs="server.crt",cert_reqs=ssl.CERT_REQUIRED)
ssl_sock.connect((Host, Port))
print repr(ssl_sock.getpeercert())
ssl_sock.write('hello, world')
data=ssl_sock.read(1024)
print ("received", data, "from server", Host)
#ssl_sock.close()
clientsocket.close()
