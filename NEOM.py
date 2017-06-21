##+"""
##+    Main function of the client with GUI
##+    Author: Ex7755(Braian)
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
    serChato = pyqtSignal()
    geraImg = pyqtSignal()
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
    def sendvib(self):
        self.sent = 22
    def sendfil(self,filee):
        self.filee = filee
        self.sent = 23
    def sendimage(self,imgf):
        self.imgf = imgf
        self.sent = 24
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
                    data = sock.recv(262144)
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
                            self.mensTe.append("\r%s:\n%s"%(user,msg))
                        elif cmd[0] == "userIn":
                            self.mensTe.append("\r%s:\n%s"%(user,msg))
                            self.contaTe.append(msg.split(" ")[0]+"\n")
                        elif cmd[0] == "userOut":
                            self.mensTe.append("\r%s:\n%s"%(user,msg))
                            tempCont = self.contaTe.toPlainText()
                            tempCont.replace('\n'+msg.split(" ")[1]+'\n',"")
                            self.progressEvent.emit(tempCont)
                        elif cmd[0] == "newFile":
                            self.mensTe.append("\r%s:\n%s"%(user,msg))
                            indata.readDocument("savedDocuments/")
                        elif cmd[0] == "newPicture":
                            self.mensTe.append("\r%s:\n%s"%(user,msg))
                            self.imgPa = indata.readDocument("savedDocuments/")
                            self.geraImg.emit()
                        elif cmd[0] == "chato":
                            self.serChato.emit()
                        else:
                            self.mensTe.append("\r%s:\n%s"%(user,msg))
                            

                # user entered a message
                else:
                    if self.sent == 21:
                        out = MessageHandler()
                        out.addMessage(self.mens)
                        out.addName(self.username)
                        self.sent = 0
                        self.ssl_sock.send(out.sendMessage())
                    elif self.sent == 22:
                        out = MessageHandler()
                        out.addOther("chato")
                        out.addMessage(" ")
                        out.addName(self.username)
                        self.sent = 0
                        self.ssl_sock.send(out.sendMessage())
                    elif self.sent == 23:
                        out = MessageHandler()
                        out.addMessage("enviou um arquivo.")
                        out.addOther("newFile")
                        out.addName(self.username)
                        out.addDocument(self.filee)
                        self.sent = 0
                        self.mensTe.append("\r%s:\n%s"%(self.username,"enviou um arquivo."))
                        self.ssl_sock.send(out.sendMessage())
                    elif self.sent == 24:
                        out = MessageHandler()
                        out.addDocument(self.imgf)
                        out.addMessage("enviou uma imagem.")
                        out.addOther("newPicture")
                        out.addName(self.username)
                        self.mensTe.append("\r%s:\n%s"%(self.username,"enviou uma imagem."))
                        self.ssl_sock.send(out.sendMessage())
                        self.sent = 0
        out = MessageHandler()
        out.addMessage("QUIT")
        out.addName(self.username)
        self.ssl_sock.send(out.sendMessage())
class ChatJan(QWidget):
    def defineThre(self,thre):
        self.thre = thre
    def closeEvent(self,event):
        self.thre.close()
def chat(myName,serverIp,serverPort,app,geo, ssl_sock,users):
    def tremer():
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
    def bAten_clicked():
        client.sendvib()
        tremer()
        
    def bEnv_clicked():
        mensagem =  str(textEnv.toPlainText())
        client.recieve(mensagem)
        mensTe.append("\r%s:\n%s\n"%(myName,mensagem))
        textEnv.clear()
    def bEnvFile_clicked():
        fileDiag = QFileDialog()
        fileDiag.setFilter(fileDiag.filter() | QDir.Hidden)
        fileDiag.setDefaultSuffix('*')
        fileDiag.setAcceptMode(QFileDialog().AcceptSave)
        fileDiag.setNameFilters(['*(*.*)'])
        filename = str(fileDiag.getOpenFileName(w,'Open File','/'))
        if fileDiag.selectedFiles():
            client.sendfil(filename)
    def showImg(filename):
        print filename
        showImg = QDialog()
        palette = QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap(filename)))
        showImg.setPalette(palette)
        showImg.setFixedSize(QPixmap(filename).width(),QPixmap(filename).height())
        showImg.exec_()
    def bEnvImg_clicked():
        fileDiag = QFileDialog()
        fileDiag.setNameFilters(["Imagens (*.png *jpg)"])
        filename = str(fileDiag.getOpenFileName(w,'Open File','/'))
        if fileDiag.selectedFiles():
            client.sendimage(filename)
            showImg(filename)
    def onResize(event):
        palette = QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap("fk-neon.jpg").scaled(w.size())))
        w.setPalette(palette)
    def remakeCont(newCont):
        contaTe.clear()
        contaTe.append(newCont)
    def keyEven(event):
            if event.key() == Qt.Key_Return:
                bEnv_clicked()
    def receberImg():
        showImg(str(client.imgPa))
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
        contaTe.append(users+"\n")

    textEnv = QTextEdit(w)
    textEnv.keyReleaseEvent = keyEven
    
    bAten = QPushButton(w)
    bAten.setText("Chamar a atencao")
    bAten.clicked.connect(bAten_clicked)

    bEnvFile = QPushButton(w)
    bEnvFile.setText("Enviar arquvo")
    bEnvFile.clicked.connect(bEnvFile_clicked)

    bEnv = QPushButton(w)
    bEnv.setText("Enviar")
    bEnv.clicked.connect(bEnv_clicked)

    bEnvImg = QPushButton(w)
    bEnvImg.setText("Enviar imagem")
    bEnvImg.clicked.connect(bEnvImg_clicked)

    grid1 = QGridLayout()
    grid1.addWidget(contaTi,1,1,Qt.AlignCenter)
    grid1.addWidget(contaTe,2,1,-1,2)
    grid1.addWidget(mensTi,1,3,Qt.AlignCenter)
    grid1.addWidget(mensTe,2,3)

    grid2 = QGridLayout()
    grid2.addWidget(textEnv,3,1,4,1)
    grid2.addWidget(bAten,3,2)
    grid2.addWidget(bEnvFile,4,2)
    grid2.addWidget(bEnvImg,5,2)
    grid2.addWidget(bEnv,6,2)

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
    client.serChato.connect(tremer)
    client.geraImg.connect(receberImg)
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
        try:
            temp = False
            errMens = None
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
                    errMens =  "Falha ao tentar conectar no servidor"
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
                        data = sock.recv(262144)
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
                                errMens =  "Nao foi possivel executar comando:\n%s" % (text)
                                ans = True
                                break
                            errMens =  "Resposta nao pode ser executada."
                            ans = True
                            break
        except:
                errMens = "Servidor nao encontrado"
                print errMens
                ans = True
        if (temp):
            w.close()
            chat(myName,serverIp,serverPort,app,w.geometry(), ssl_sock,users)
        else:
            print errMens
            errMensq = QMessageBox(None)
            errMensq.setIcon(QMessageBox.Warning)
            errMensq.setText(errMens)
            errMensq.exec_()
    def bRes_clicked():
        new  = True
        bCo_clicked(new)
    def onResize(event):
        palette = QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap("abstract-neon.jpg").scaled(w.size())))
        w.setPalette(palette)
    w = QWidget()
    w.resizeEvent = onResize
    subT = QLabel(w)
    subT.setText("Digite o ip do servidor:")
    subT.setStyleSheet("color: white")
    subTP = QLabel(w)
    subTP.setText("Digite a porta do servidor:")
    subTP.setStyleSheet("color: white")
    subTU = QLabel(w)
    subTU.setText("Digite o nome de usuario:")
    subTU.setStyleSheet("color: white")
    subTUS = QLabel(w)
    subTUS.setText("Digite a senha:")
    subTUS.setStyleSheet("color: white")
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
    w.setMinimumSize(200,350)
    palette = QPalette()
    palette.setBrush(QPalette.Background,QBrush(QPixmap("abstract-neon.jpg").scaled(w.size())))
    w.setPalette(palette)
    w.setWindowTitle("NEOM")
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    start(app)
    sys.exit()
