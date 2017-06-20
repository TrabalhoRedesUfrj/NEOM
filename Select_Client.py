import socket, select, string, sys, ssl, pprint
from Protocol import MessageHandler

ssl_certfile = "./keys/server.crt"

def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()

username = 'meunome'
senha = 'ehzoado'
new = False

# main function
if __name__ == "__main__":

    if (len(sys.argv) < 3):
        print 'Usage : python telnet.py hostname port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    ssl_sock=ssl.wrap_socket(s,ca_certs=ssl_certfile,cert_reqs=ssl.CERT_REQUIRED)

    # connect to remote host
    try:
        ssl_sock.connect((host, port))
        print repr(ssl_sock.getpeername())
        print ssl_sock.cipher()
        print pprint.pformat(ssl_sock.getpeercert())
    except:
        print 'Unable to connect'
        sys.exit()

    auth = MessageHandler()
    ssl_sock.send(auth.sendAuthentication(username, senha, new=new))
    ans = False
    socket_list = [sys.stdin, ssl_sock]
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
    # Wait for answer from server
    while not ans:
        for sock in read_sockets:
            if sock == ssl_sock:
                data = sock.recv(4096)
                if data:
                    auth.cleanAll()
                    auth.receiveMessage(data)
                    commands = auth.readOther()
                    if "authenticate" in commands:
                        if "ok" in commands:
                            ans = True
                            users = auth.readMessage()
                            if users:
                                users = users.split(',')
                            break
                        elif "fail" in commands:
                            text = auth.readMessage()
                            print "Could not execute command:\n%s" % (text)
                            sys.exit()
                            prompt()
                            ans = True
                            break
                        print "Error: Response could not be interpreted."
                        sys.exit()
                        prompt()
                        ans = True
                    break

    print 'Connected to remote host. Start sending messages'
    print 'Type (QUIT) in msg to exit chat'
    prompt()

    while 1:
        socket_list = [sys.stdin, ssl_sock]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        for sock in read_sockets:
            # incoming message from remote server
            if sock == ssl_sock:
                data = sock.recv(4096)
                if not data:
                    print '\nDisconnected from chat server'
                    sys.exit()
                else:
                    # print data
                    indata = MessageHandler()
                    indata.receiveMessage(data)
                    msg = indata.readMessage()
                    user = indata.readName()
                    sys.stdout.write("\r<%s> %s"%(user,msg))
                    prompt()

            # user entered a message
            else:
                out = MessageHandler()
                msg = sys.stdin.readline()
                out.addMessage(msg)
                out.addName(username)
                ssl_sock.send(out.sendMessage())
                if "QUIT" in msg:
                    sys.exit()
                prompt()