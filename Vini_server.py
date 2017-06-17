#!/usr/bin/python3
import socket, sys, threading
from socket import *
import ssl

PORT = 50127


# Simple chat client that allows multiple connections via threads

class ChatServer(threading.Thread):
    def __init__(self, port, host='localhost'):
        threading.Thread.__init__(self)
        self.port = port
        self.host = host
        self.server = socket(AF_INET, SOCK_STREAM)
        # self.server.setblocking(0)
        self.users = {}  # current connections
        self.inputs = [self.server]
        self.outputs = []
        try:
            self.server.bind((self.host, self.port))

        except:
            print('Bind failed %s')
            sys.exit()

    # Not currently used. Ensure sockets are closed on disconnect
    def exit(self):
        self.server.close()

    def run_thread(self, connection, addr):
        print('Client connected with ' + addr[0] + ':' + str(addr[1]))
        while True:
            data = connection.recv(1024)
            if not data:
                break
            print(data)
            reply = 'OK Im listening you    ...' + str(addr)
            print('sending reply :' + reply)
            connection.send(reply)
        connection.close()  # Close

    def run(self):
        self.server.listen(5)
        print('Waiting for connections on port %s' % (self.port))
        # We need to run a loop and create a new thread for each connection
        while True:
            (connectionsocket, addr) = self.server.accept()
            #criptosocket =ssl.wrap_socket(connectionsocket,server_side=True)
            threading.Thread(target=self.run_thread, args=(connectionsocket, addr)).start()


class ChatClient(object):
    def __init__(self, port, host='localhost'):
        self.host = host
        self.port = port
        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.connect((self.host, self.port))

    def send_message(self, msg):
        pass


if __name__ == '__main__':
    server = ChatServer(PORT, '127.0.0.5')
    # Run the chat server listening on PORT
    server.run()
