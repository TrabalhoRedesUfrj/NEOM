"""
    Message Handler Protocol
    Author: Amanda
"""
__all__ = ['MessageHandler']


# Onde colocar tratamento de caracteres especiais??

class MessageHandler():
    # TODO: Add other possible data
    def __init__(self):
        self.cleanAll()

    def cleanAll(self):
        self.text = ""
        self.picture = None
        # self.audio = None
        # self.site = None
        # self.document = None
        self.other = []

    def addMessage(self, text):
        self.text = text

    def addPicture(self, picture):
        import base64
        with open(picture, "rb") as imgFile:
            st = base64.b64encode(imgFile.read())
            self.picture = st

    def addOther(self, other):
        self.other += [other]

    def sendMessage(self):
        import json
        attrDict = {
                        'text': self.text,
                        'other': self.other,
                        'picture': self.picture
                    }
        return json.dumps(attrDict)

    def recieveMessage(self, binary):
        self.cleanAll()
        import json
        attrDict = json.loads(binary)
        self.text = attrDict[u'text']
        self.other = attrDict[u'other']
        self.picture = attrDict[u'picture']

    def readMessage(self):
        if len(self.text)==0: return None
        return self.text

    def readPicture(self, path=""):
        if not self.picture: return None
        import time
        data = "_%s_%1.2i:%1.2i"%(time.strftime("%d_%m_%Y"),
                                  time.localtime(time.time()).tm_hour,
                                  time.localtime(time.time()).tm_min)
        img = "%ssavedImage%s.png"%(path,data)
        fh = open(img, "wb")
        fh.write(self.picture.decode('base64'))
        fh.close()
        return img


    def readOther(self):
        if len(self.other)==0: return None
        return self.other

