"""
    Test of Message Handler Protocol features
    Sending documents
    Author: Amanda
"""
# import webbrowser
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))

from Protocol import MessageHandler

pathToSaveFiles = ""

fileName = "Julia_install.pdf"
message = "Everything you need to know to install Julia"

msgS = MessageHandler()
msgS.addMessage(message)
msgS.addDocument(fileName)
pkg = msgS.sendMessage()

msgC = MessageHandler()
msgC.recieveMessage(pkg)

text = msgC.readMessage()
commands = msgC.readOther()
picture = msgC.readPicture(pathToSaveFiles)
fileName = msgC.readDocument(pathToSaveFiles)
if fileName:
    print "Document received: %s"%(fileName)
    # TODO: Print file content
    # f = open('tmp.html', 'w')
    # message = """<html>
    # <head><p>File View</p></head>
    # <body></body>
    # <a href="%s"></a>
    # </html>""" % (fileName)
    # f.write(message)
    # f.close()
    # wepPage = 'tmp.html'
    # webbrowser.open_new_tab(os.getcwd() + '/' + wepPage)
if text: print "Message Received: %s"%(text)


# Since this is only a file to test the file transfer, we delete
# the file in order to not have memory overload
os.remove(fileName)
# os.remove(wepPage)
print "File deleted"
