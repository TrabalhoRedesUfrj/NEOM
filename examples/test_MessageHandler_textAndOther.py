#!/usr/bin/python
# -*- coding: latin-1 -*-
"""
    Test of Message Handler Protocol features
    Usage of text message and chat commands
    Author: Amanda
"""
import sys, os
import emoji
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))

from Protocol import MessageHandler

message = "Oie!\nÉ legal testar os caracteres! E se você mandar a mensagem e ela não chegar direito?\n:wink:"
command = "chato"

msgS = MessageHandler()
msgS.addMessage(message)
msgS.addOther(command)
pkg = msgS.sendMessage()

msgC = MessageHandler()
msgC.receiveMessage(pkg)

# print pkg

text = msgC.readMessage()
commands = msgC.readOther()
if text:
    try:
        print emoji.emojize('Message Received:\n%s'%(text), use_aliases=True)
    except UnicodeDecodeError:
        print 'Message Received:\n%s'%(text)
if commands:
    for cm in commands:
        print "Execute command '%s'"%(cm)