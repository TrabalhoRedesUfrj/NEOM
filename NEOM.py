import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from random import randint
import time

def chat(myName,ServerIp,app,geo):
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
        mensagem = textEnv.toPlainText()
        textEnv.clear()
        print "vixe, a mensagem " + mensagem+ " foi enviada!"

        ########CODIGO DE ENVIO DE MENSAGEM AQUI DIACHO








        #########
    w = QWidget()
    userT = QLabel(w)
    userT.setText("Usuario: " + myName)
    conneT = QLabel(w)
    conneT.setText("Conectado a: "+ ServerIp)
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

    
    w.setGeometry(geo.x(),geo.y(),500,500)
    w.setWindowTitle("NEOM")
    w.show()

    
def start():
    
    def bCo_clicked():
        ServerIp = textT.text()
        myName = textTU.text()
        w.close()
        chat(myName,ServerIp,app,w.geometry())
        
    app = QApplication(sys.argv)
    w = QWidget()
    subT = QLabel(w)
    subT.setText("Digite o ip do servidor:")
    subTU = QLabel(w)
    subTU.setText("Digite o nome de usurario:")
    textT = QLineEdit(w)
    textTU = QLineEdit(w)

    bCo = QPushButton(w)
    bCo.setText("Conectar")
    bCo.clicked.connect(bCo_clicked)

    vbox = QVBoxLayout()
    vbox.addWidget(subTU)
    vbox.addWidget(textTU)
    vbox.addWidget(subT)
    vbox.addWidget(textT)
    vbox.addWidget(bCo)
    vbox.addStretch(1)

    hbox = QHBoxLayout()
    hbox.addStretch(1)
    hbox.addLayout(vbox)
    hbox.addStretch(1)
    w.setLayout(hbox)

    
    w.setGeometry(200,200,200,100)
    w.setWindowTitle("NEOM")
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    start()
