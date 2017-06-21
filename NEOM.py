##+"""
##+    Main function of the client with GUI
##+    Author: Ex7755
##+"""

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from random import randint
import time
import socket, select, string, sys, ssl, pprint
from Protocol import MessageHandler
ssl_certfile = "./keys/server.crt"

class ClientThread(QThread):
    progressEvent = pyqtSignal(QString)
    def __init__(self,contaTe,mensTe, textEnv, ssl_sock,username,w):
        QThread.__init__(self)
        self.contaTe = contaTe
        self.mensTe = mensTe
        self.textEnv = textEnv
        self.ssl_sock = ssl_sock
        self.sent = 0
        self.mens = ""
        self.username = username
        self.w = w
    def recieve(self,mens):
        self.mens = mens
        self.sent = 21
    def close(self):
        self.runT = False
    def run(self):
        self.runT = True
        while self.runT:
            socket_list = [self.sent,self.ssl_sock]
            # Get the list sockets which are readable
            read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
            
            for sock in read_sockets:
                # incoming message from remote server
                if sock == self.ssl_sock:
                    data = sock.recv(4096)
                    if not data:
                        print '\nDisconnected from chat server'
                        self.w.close()
                        self.runT = False
                    else:
                        indata = MessageHandler()
                        indata.receiveMessage(data)
                        cmd = indata.readOther()
                        msg = indata.readMessage()
                        user = indata.readName()
                        if cmd == None:
                            self.mensTe.append("\r%s:\n%s\n"%(user,msg))
                        elif cmd[0] == "userIn":
                            self.mensTe.append("\r%s:\n%s\n"%(user,msg))
                            self.contaTe.append(msg.split(" ")[0]+"\n")
                        elif cmd[0] == "userOut":
                            self.mensTe.append("\r%s:\n%s\n"%(user,msg))
                            tempCont = self.contaTe.toPlainText()
                            tempCont.replace('\n'+msg.split(" ")[1]+'\n',"")
                            self.progressEvent.emit(tempCont)
                        elif cmd[0] == "newFile":
                            self.mensTe.append("\r%s:\n%s\n"%(user,msg))
                        elif cmd[0] == "chato":
                            print "sou chato"
                        else:
                            self.mensTe.append("\r%s:\n%s\n"%(user,msg))
                            

                # user entered a message
                else:
                    if(self.sent != 0):
                        
                        out = MessageHandler()
                        out.addMessage(self.mens)
                        out.addName(self.username)
                        self.sent = 0
                        self.ssl_sock.send(out.sendMessage())
        out = MessageHandler()
        out.addMessage("QUIT")
        self.ssl_sock.send(out.sendMessage())
class ChatJan(QWidget):
    def defineThre(self,thre):
        self.thre = thre
    def closeEvent(self,event):
        self.thre.close()
        
def chat(myName,serverIp,serverPort,app,geo, ssl_sock,users):
    def bAten_clicked():
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
        mensagem =  str(textEnv.toPlainText())
        client.recieve(mensagem)
        mensTe.append("\r%s:\n%s\n"%(myName,mensagem))
        textEnv.clear()

    def onResize(event):
        palette = QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap("fk-neon.jpg").scaled(w.size())))
        w.setPalette(palette)
    def remakeCont(newCont):
        contaTe.clear()
        contaTe.append(newCont)
    w = ChatJan()
    w.resizeEvent = onResize
    userT = QLabel(w)
    userT.setText("Usuario: " + myName)
    userT.setStyleSheet("color: white")
    conneT = QLabel(w)
    conneT.setText("Conectado a: "+ serverIp +":")
    conneT.setStyleSheet("color: white")
    mensTi = QLabel(w)
    mensTi.setText("Mensagens")
    mensTi.setStyleSheet("color: white")
    mensTe = QTextEdit(w)
    mensTe.setReadOnly(True)
    
    contaTi = QLabel(w)
    contaTi.setText("Usuarios conectados")
    contaTi.setStyleSheet("color: white")
    contaTe = QTextEdit(w)
    contaTe.setReadOnly(True)
    
    contaTe.append(myName+"\n")
    if (users != "None"):
        contaTe.append(users)

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
    
    client = ClientThread(contaTe,mensTe, textEnv, ssl_sock,myName,w)
    client.progressEvent.connect(remakeCont)
    palette = QLabel()
    w.defineThre(client)
    w.setGeometry(geo.x(),geo.y(),800,500)
    w.setMinimumSize(800,500)
    palette = QPalette()
    palette.setBrush(QPalette.Background,QBrush(QPixmap("fk-neon.jpg").scaled(w.size())))
    w.setPalette(palette)
    w.setWindowTitle("NEOM")
    w.show()
    client.start()

    
def start(app):
        
    def bCo_clicked(new):
        temp = False
        try:
            serverIp = str(textT.text())
            serverPort = int(textTP.text())
            myName = str(textTU.text())
            myPass = str(textTUS.text())
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            ssl_sock=ssl.wrap_socket(s,ca_certs=ssl_certfile,cert_reqs=ssl.CERT_REQUIRED)
            try:
                ssl_sock.connect((serverIp,serverPort))
            except:
                print "Falha ao tentar conectar no servidor"
        except:
            print "dados invalidos"
        auth = MessageHandler()
        ssl_sock.send(auth.sendAuthentication(myName, myPass, new=new))
        ans = False
        socket_list = [ssl_sock]
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
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
                            temp = True
                            users = str(auth.readMessage())
                            users = users.replace(',','\n')
                        
                            break
                        elif "fail" in commands:
                            text = auth.readMessage()
                            print "Could not execute command:\n%s" % (text)
                            ans = True
                            break
                        print "Error: Response could not be interpreted."
                        ans = True
                        break
        if (temp):
            w.close()
            chat(myName,serverIp,serverPort,app,w.geometry(), ssl_sock,users)
    def bRes_clicked():
        new  = True
        bCo_clicked(new)
    w = QWidget()
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

    new = False
    w.setGeometry(200,200,200,300)
    w.setMinimumSize(200,300)
    
    w.setWindowTitle("NEOM")
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    start(app)
    sys.exit()
