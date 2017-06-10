"""
    Test of Message Handler Protocol features
    Usage of text message and chat commands
    Author: Amanda
"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))

from Protocol import MessageHandler

message = "Hi, there!"
command = "chato"

msgS = MessageHandler()
msgS.addMessage(message)
msgS.addOther(command)
pkg = msgS.sendMessage()

msgC = MessageHandler()
msgC.recieveMessage(pkg)

# print pkg

text = msgC.readMessage()
commands = msgC.readOther()
if text: print "Message Received: %s"%(text)
if commands:
    for cm in commands:
        print "Execute command '%s'"%(cm)