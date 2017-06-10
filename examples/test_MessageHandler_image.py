"""
    Test of Message Handler Protocol feamv ts   tures
    Sending pictures
    Author: Amanda
"""
import sys, os
# from PIL import Image
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))

from Protocol import MessageHandler

onePic = False

pathToSavePictures = ""

picture = "Stickerline-elsa-let-it-go.png"
if not onePic:
    picture = [picture, "busto-display-aplique-elsa-frozen-10cm-tag.jpg"]
message = "The cold never bothered me anyway"

msgS = MessageHandler()
msgS.addMessage(message)
msgS.addPicture(picture)
pkg = msgS.sendMessage()

msgC = MessageHandler()
msgC.recieveMessage(pkg)

text = msgC.readMessage()
commands = msgC.readOther()
pictures = msgC.readPicture(pathToSavePictures)
if pictures:
    for pic in pictures:
        print "Image received: %s"%(pic)
        # TODO: Print image on screen before deleting it
        # img = Image.open(picture)
        # img.show()
if text: print "Message Received: %s"%(text)
if commands:
    for cm in commands:
        print "Execute command '%s'"%(cm)

# Since this is only a file to test the image transfer, we delete
# the image in order to not have memory overload
for pic in pictures:
    os.remove(pic)
print "Picture deleted"