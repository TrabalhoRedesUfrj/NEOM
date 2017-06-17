from socket import *
import sys
import ssl
import select
from thread import *

class TCPConection:
    def __init__(self,servidor,porta):
        self.servidor=servidor
        self.porta=porta

        #Create a TCP/IP Socket
        self.sock=socket(AF_INET,SOCK_STREAM)
        self.sock.setblocking(0)

        self.adress=('127.0.0.5',50007)
        self.inputs=[self.sock]
        self.outputs=[]
        #Outgoing Message queues
        self.message_queues={}







