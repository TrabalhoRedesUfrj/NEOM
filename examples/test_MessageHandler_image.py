"""
    Test of Message Handler Protocol features
    Sending pictures
    Author: Amanda
"""
import sys, os
# from PIL import Image
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))

from Protocol import MessageHandler

pathToSavePictures = ""

picture = "Stickerline-elsa-let-it-go.png"
message = "The cold never bothered me anyway"

msgS = MessageHandler()
msgS.addMessage(message)
msgS.addPicture(picture)
pkg = msgS.sendMessage()

msgC = MessageHandler()
msgC.recieveMessage(pkg)

text = msgC.readMessage()
commands = msgC.readOther()
picture = msgC.readPicture(pathToSavePictures)
if picture:
    print "Image received: %s"%(picture)
    # TODO: Print image on screen before deleting it
    # img = Image.open(picture)
    # img.show()
if text: print "Message Received: %s"%(text)
if commands:
    for cm in commands:
        print "Execute command '%s'"%(cm)

# Since this is only a file to test the image transfer, we delete
# the image in order to not have memory overload
os.remove(picture)
print "Picture deleted"