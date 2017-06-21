"""
    Server helping classes and functions
    Author: vini
"""
__all__ = ['TCPBase',
           'ServerThread',
           'broadcast_data',
           'quitConnection']

import socket
import threading
from Protocol import MessageHandler

class TCPBase(threading.Thread):
    def __init__(self):
        super(TCPBase, self).__init__()
        self.soc = self.buildSocket()

    def buildSocket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print 'Socket created'
        except socket.error, msg:
            print 'Failed to create socket Error code: ' + str(msg[0]) + ', Error message: ' + msg[1]
        return s

    def printErr(self, usrMsg, msg):
        print usrMsg
        print msg

class ServerThread(TCPBase):
        def __init__(self):
            super(ServerThread, self).__init__()

        def run(self, port):
            self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            err = 0
            msg = None
            try:
                self.soc.bind(("0.0.0.0", port))
                print "Bind worked\n"
            except socket.error, msg:
                print "Bind failed in server: " + str(msg[0]) + " Message " + msg[1]
                err = 1
            if not err:
                try:
                    self.soc.listen(10)
                except socket.error, msg:
                    print "Listen failed: " + str(msg[0]) + " Message " + msg[1]
                    err = 1


# Function to broadcast chat messages to all connected clients
def broadcast_data(sock, message, connection_list, server_sock):
    # Do not send the message to master socket and the client who has send us the message
    for socket in connection_list:
        if socket != server_sock.soc and socket != sock:
            try:
                socket.send(message)
            except:
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                connection_list.remove(socket)


def quitConnection(sock, address, connection_list, users, server_sock):
    print "I'm quitting"
    out = MessageHandler()
    out.addName("Server")
    out.addOther("userOut")
    out.addMessage("Client %s %s is offline \n" % (users[address], str(address)))
    print "Client %s %s is offline" % (users[address], str(address))
    connection_list.remove(sock)
    users.pop(address)
    broadcast_data(sock, out.sendMessage(), connection_list, server_sock)
    sock.close()