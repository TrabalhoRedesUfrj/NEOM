import socket, select, string, sys, ssl, pprint

ssl_certfile = "/home/vini/TrabalhoRedes1/NEOM/server.crt"

def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()

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

    print 'Connected to remote host. Start sending messages'
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
                    sys.stdout.write(data)
                    prompt()

            # user entered a message
            else:
                msg = sys.stdin.readline()
                ssl_sock.send(msg)
                if "QUIT" in msg:
                    sys.exit()
                prompt()