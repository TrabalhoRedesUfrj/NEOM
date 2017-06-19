#!/usr/bin/python

# TCP Chat server
import socket, select
import threading
import ssl

ssl_keyfile = "./keys/server.key"
ssl_certfile = "./keys/server.crt"

try:
    ipAddr = socket.gethostbyname("localhost")
    print "IP = " + ipAddr
except socket.gaierror:
    print "Host name could not be resolved"


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
        print usrMsg

class ServerThread(TCPBase):
        def __init__(self):
            super(ServerThread, self).__init__()

        def run(self):
            self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            err = 0
            msg = None
            try:
                self.soc.bind(("0.0.0.0", PORT))
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
def broadcast_data(sock, message):
    # Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket.soc and socket != sock:
            try:
                socket.send(message)
            except:
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)


if __name__ == "__main__":

    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096  # Advisable to keep it as an exponent of 2
    PORT = 5000

    server_socket = ServerThread()
    server_socket.run()

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket.soc)

    print "Chat server started on port " + str(PORT)

    while True:
        # Get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])

        for sock in read_sockets:
            # New connection
            if sock == server_socket.soc:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.soc.accept()
                ssl_sock=ssl.wrap_socket(sockfd,server_side=True,certfile=ssl_certfile,keyfile=ssl_keyfile)
                CONNECTION_LIST.append(ssl_sock)
                print "Client (%s, %s) connected" % addr

                broadcast_data(ssl_sock, "[%s:%s] entered room\n" % addr)

            # Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    # In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)
                    if "QUIT" in data:
                        raise
                except:
                    broadcast_data(sock, "Client (%s, %s) is offline \n" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

    server_socket.soc.close()
