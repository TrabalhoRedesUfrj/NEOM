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
        self.document = None
        self.other = []

    def addMessage(self, text):
        self.text = text

    def addPicture(self, picture):
        import base64
        if not isinstance(picture, (list,tuple)): picture = [picture]
        pics = []
        for pic in picture:
            with open(pic, "rb") as imgFile:
                st = base64.b64encode(imgFile.read())
                pics += [st]
        self.picture = pics

    def addDocument(self, doc):
        # Can be used to transfer any kind of document
        import base64
        docType = doc.split('.')[-1]
        with open(doc, "rb") as docFile:
            docStr = base64.b64encode(docFile.read())
            self.document = [docStr, docType]

    def addOther(self, other):
        self.other += [other]

    def sendMessage(self):
        import json
        attrDict = {
                        'text': self.text,
                        'other': self.other,
                        'picture': self.picture,
                        'document': self.document
                    }
        return json.dumps(attrDict)

    def recieveMessage(self, binary):
        self.cleanAll()
        import json
        attrDict = json.loads(binary)
        self.text = attrDict[u'text']
        self.other = attrDict[u'other']
        self.picture = attrDict[u'picture']
        self.document = attrDict[u'document']

    def readMessage(self):
        if len(self.text)==0: return None
        return self.text

    def readPicture(self, path="", client = None):
        if not self.picture: return None
        import time
        pics = []
        for i in range(len(self.picture)):
            pic = self.picture[i]
            data = "_%s_%1.2i:%1.2i_%i"%(time.strftime("%d_%m_%Y"),
                                            time.localtime(time.time()).tm_hour,
                                            time.localtime(time.time()).tm_min,
                                            i)
            img = "%ssavedImage%s.png"%(path,data)
            if client:
                img = "%s_%s"%(client,img)
            fh = open(img, "wb")
            fh.write(pic.decode('base64'))
            fh.close()
            pics += [img]
        return pics

    def readDocument(self, path="", client = None):
        if not self.document: return None
        import time
        data = "_%s_%1.2i:%1.2i"%(time.strftime("%d_%m_%Y"),
                                  time.localtime(time.time()).tm_hour,
                                  time.localtime(time.time()).tm_min)
        doc = "%ssavedFile%s.%s"%(path,data,self.document[1])
        if client:
            doc = "%s_%s"%(client,doc)
        fh = open(doc, "wb")
        fh.write(self.document[0].decode('base64'))
        fh.close()
        return doc

    def readOther(self):
        if len(self.other)==0: return None
        return self.other
