#!/usr/bin/python

# TCP Chat server
import socket, select
import ssl
from Server import *
from Protocol import *

ssl_keyfile = "./keys/server.key"
ssl_certfile = "./keys/server.crt"
userfile = "./keys/neom_users.pic.tz"

try:
    ipAddr = socket.gethostbyname("localhost")
    print "IP = " + ipAddr
except socket.gaierror:
    print "Host name could not be resolved"

if __name__ == "__main__":

    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096  # Advisable to keep it as an exponent of 2
    PORT = 5000

    server_socket = ServerThread()
    server_socket.run(PORT)

    # User Authentication
    users = UserAuthentication(userfile)
    usernames = {}

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
                try:
                    connect = False
                    sockfd, addr = server_socket.soc.accept()
                    ssl_sock = ssl.wrap_socket(sockfd,server_side=True,certfile=ssl_certfile,keyfile=ssl_keyfile)
                    auth = MessageHandler()
                    data = ssl_sock.recv(RECV_BUFFER)
                    if data:
                        auth.receiveMessage(data)
                        commands = auth.readOther()
                        if "authenticate" in commands:
                            out = MessageHandler()
                            out.addOther("authenticate")
                            check = auth.readAuthentication()
                            for ad in usernames.keys():
                                if check['user'] == usernames[ad]:
                                    out.addOther("fail")
                                    out.addMessage("User already connected, cannot connect again.")
                                    print "%s tried another connection. Should change password?"%(check['user'])
                                    ssl_sock.send(out.sendMessage())
                                    ssl_sock.close()
                            if "add" in commands:
                                try:
                                    users.addUser(check['user'], check['password'])
                                    out.addOther("ok")
                                    print "Added user %s"%(check['user'])
                                    connect = True
                                except NameError:
                                    out.addOther("fail")
                                    out.addMessage("User already used. Choose another.")
                                    ssl_sock.send(out.sendMessage())
                                    ssl_sock.close()
                            elif "rm" in commands:
                                text = users.rmUser(check['user'], check['password'])
                                if text == "User removed":
                                    out.addOther("ok")
                                    connect = True
                                else:
                                    out.addOther("fail")
                                    if text == "Wrong Password":
                                        out.addMessage("%s. Try again." % (text))
                                    elif text == "No user":
                                        out.addMessage("%s found. Try again." % (text))
                                    ssl_sock.send(out.sendMessage())
                                    ssl_sock.close()
                            else:
                                text = users.checkUser(check['user'], check['password'])
                                if text == "User verified":
                                    out.addOther("ok")
                                    connect = True
                                else:
                                    out.addOther("fail")
                                    if text == "Wrong Password":
                                        out.addMessage("%s. Try again." % (text))
                                    elif text == "No user":
                                        out.addMessage("%s found. Try again." % (text))
                                    ssl_sock.send(out.sendMessage())
                                    ssl_sock.close()
                            if connect:
                                first = True
                                text = ""
                                for key in usernames.keys():
                                    if first:
                                        text += "%s"%(usernames[key])
                                        first = False
                                    else:
                                        text += ",%s"%(usernames[key])
                                out.addMessage(text)
                            ssl_sock.send(out.sendMessage())
                    if connect:
                        CONNECTION_LIST.append(ssl_sock)
                        usernames[addr] = check['user']
                        print "Client %s %s connected" % (usernames[addr],str(addr))
                        out.cleanAll()
                        out.addName("Server")
                        out.addOther("userIn")
                        out.addMessage("%s %s entered room\n" % (usernames[addr],str(addr)))
                        broadcast_data(ssl_sock, out.sendMessage(), CONNECTION_LIST, server_socket)
                except:
                    pass

            # Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    # In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    out = MessageHandler()
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        out.receiveMessage(data)
                        if out.readOther():
                            if "authenticate" in out.readOther():
                                continue
                        if "QUIT" == out.readMessage():
                            raise
                        else:
                            if usernames[sock.getpeername()] != out.readName():
                                print "Something wrong with the client!! It has forgotten it's own name!! :scream:"
                            broadcast_data(sock, data, CONNECTION_LIST, server_socket)
                except:
                    out = MessageHandler()
                    out.addName("Server")
                    out.addOther("userOut")
                    out.addMessage("Client %s %s is offline \n" % (usernames[addr],str(addr)))
                    broadcast_data(sock, out.sendMessage(), CONNECTION_LIST, server_socket)
                    print "Client %s %s is offline" % (usernames[addr],str(addr))
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    usernames.pop(addr)
                    continue

    server_socket.soc.close()