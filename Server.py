# -*- coding: utf-8 -*-
"""
Created on Tue May 30 19:42:34 2017
@author: vini
"""
Host='127.0.0.5'
Port=50007
from socket import socket, AF_INET, SOCK_STREAM
serversocket = socket(AF_INET,SOCK_STREAM)
serversocket.bind((Host, Port))
print ("using", serversocket.getsockname())
serversocket.listen(1)  #Tamanho maximo de conexões permitidas#
(connectionsocket, addr)=serversocket.accept()
print 'Conected by', addr
while True:
    data = connectionsocket.recv(1024)
    if not data:
        break
    print ("Connection from", addr)
    print ("estou aqui recebendo dado do client:", data, "from Client", addr)
    data1="Ola estou recebendo sua menssagem"
    connectionsocket.sendall(data1)
connectionsocket.close()
