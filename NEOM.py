__all__ = ['ClientThread']
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from random import randint
import time
import socket, select, string, sys, ssl, pprint
ssl_certfile = "./keys/server.crt"

class ClientThread(QThread):
    def __init__(self,contaTe,mensTe, textEnv, ssl_sock):
        QThread.__init__(self)
        self.contaTe = contaTe
        self.mensTe = mensTe
        self.textEnv = textEnv
        self.ssl_sock = ssl_sock
        self.sent = 0
        self.mens = ""
    def recieve(self,mens):
        self.mens = mens
        self.sent = 21
    def run(self):
        while 1:
            socket_list = [self.sent,self.ssl_sock]
            # Get the list sockets which are readable
            read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
            for sock in read_sockets:
                # incoming message from remote server
                if sock == self.ssl_sock:
                    data = sock.recv(4096)
                    if not data:
                        print '\nDisconnected from chat server'
                    else:
                        # print data
                        self.mensTe.append(data)

                # user entered a message
                else:
                    if(self.sent != 0):
                        print self.sent
                        self.sent = 0
                        self.ssl_sock.send(self.mens + "\n")
def chat(myName,serverIp,serverPort,app,geo, ssl_sock):
    def bAten_clicked():
        print "oia, o botao 1 foi pressionado"
        xOri = w.geometry().x()
        yOri = w.geometry().y()
        w.move(0,0)
        xD = w.geometry().x()
        yD = w.geometry().y()
        xOri = xOri - xD
        yOri = yOri - yD
        for i in range(1,100):
            w.move(xOri,yOri)
            xt = randint(-5,5)
            yt = randint(-5,5)
            w.move(xOri+xt,yOri+yt)
            app.processEvents()
            time.sleep(0.01)
        w.move(xOri,yOri)
        
    def bEnv_clicked():
        client.recieve(textEnv.toPlainText())
        textEnv.clear()
        print "vixe, a mensagem  foi enviada!"
    w = QWidget()
    #palette = QPalette()
    #palette.setBrush(QPalette.Background,QBrush(QPixmap("fk-neon.jpg")))
    #w.setPalette(palette)
    
    userT = QLabel(w)
    userT.setText("Usuario: " + myName)
    conneT = QLabel(w)
    conneT.setText("Conectado a: "+ serverIp +":")
    mensTi = QLabel(w)
    mensTi.setText("Mensagens")
    mensTe = QTextEdit(w)
    mensTe.setReadOnly(True)
    
    
    contaTi = QLabel(w)
    contaTi.setText("Usuarios conectados")
    contaTe = QTextEdit(w)
    contaTe.setReadOnly(True)

    textEnv = QTextEdit(w)
    
    
    bAten = QPushButton(w)
    bAten.setText("aporrinhar o saco")
    bAten.clicked.connect(bAten_clicked)

    bEnv = QPushButton(w)
    bEnv.setText("Enviar")
    bEnv.clicked.connect(bEnv_clicked)

    grid1 = QGridLayout()
    grid1.addWidget(contaTi,1,1,Qt.AlignCenter)
    grid1.addWidget(contaTe,2,1,-1,2)
    grid1.addWidget(mensTi,1,3,Qt.AlignCenter)
    grid1.addWidget(mensTe,2,3)

    grid2 = QGridLayout()
    grid2.addWidget(textEnv,3,1,2,1)
    grid2.addWidget(bAten,3,2)
    grid2.addWidget(bEnv,4,2)

    hbox1 = QHBoxLayout()
    hbox1.addStretch()
    hbox1.addWidget(userT)
    hbox1.addStretch()

    hbox2 = QHBoxLayout()
    hbox2.addStretch()
    hbox2.addWidget(conneT)
    hbox2.addStretch()
    
    vbox = QVBoxLayout()
    vbox.addLayout(hbox1)
    vbox.addLayout(hbox2)
    vbox.addLayout(grid1)
    vbox.addLayout(grid2)
    w.setLayout(vbox)

    client = ClientThread(contaTe,mensTe, textEnv, ssl_sock)
    client.start()
    w.setGeometry(geo.x(),geo.y(),800,500)
    w.setWindowTitle("NEOM")
    w.show()

    
def start():
    
    def bCo_clicked():
        temp = False
        try:
            serverIp = textT.text()
            serverPort = int(textTP.text())
            myName = textTU.text()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            ssl_sock=ssl.wrap_socket(s,ca_certs=ssl_certfile,cert_reqs=ssl.CERT_REQUIRED)
            try:
                ssl_sock.connect((serverIp,serverPort))
                print repr(ssl_sock.getpeername())
                print ssl_sock.cipher()
                print pprint.pformat(ssl_sock.getpeercert())
                w.close()
                temp = True
            except:
                print "Falha ao tentar conectar no servidor"
        except:
            print "dados invalidos"
        if (temp):
            chat(myName,serverIp,serverPort,app,w.geometry(), ssl_sock)
    def bRes_clicked():
        ServerIp = textT.text()
        
    app = QApplication(sys.argv)
    w = QWidget()
    #palette = QPalette()
    #palette.setBrush(QPalette.Background,QBrush(QPixmap("fk-neon.jpg")))
    #w.setPalette(palette)
    subT = QLabel(w)
    subT.setText("Digite o ip do servidor:")
    subTP = QLabel(w)
    subTP.setText("Digite a porta do servidor:")
    subTU = QLabel(w)
    subTU.setText("Digite o nome de usuario:")
    subTUS = QLabel(w)
    subTUS.setText("Digite a senha:")
    textT = QLineEdit(w)
    textTP = QLineEdit(w)
    textTU = QLineEdit(w)
    textTUS = QLineEdit(w)
    textTUS.setEchoMode(QLineEdit.Password)

    bCo = QPushButton(w)
    bCo.setText("Conectar")
    bCo.clicked.connect(bCo_clicked)
    bRes = QPushButton(w)
    bRes.setText("Registrar")
    bRes.clicked.connect(bRes_clicked)
                       
    vbox = QVBoxLayout()
    vbox.addWidget(subTU)
    vbox.addWidget(textTU)
    vbox.addWidget(subTUS)
    vbox.addWidget(textTUS)
    vbox.addWidget(subT)
    vbox.addWidget(textT)
    vbox.addWidget(subTP)
    vbox.addWidget(textTP)
    vbox.addWidget(bCo)
    vbox.addWidget(bRes)
    vbox.addStretch(1)

    hbox = QHBoxLayout()
    hbox.addStretch(1)
    hbox.addLayout(vbox)
    hbox.addStretch(1)
    w.setLayout(hbox)

    
    w.setGeometry(200,200,200,300)
    w.setWindowTitle("NEOM")
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    start()
