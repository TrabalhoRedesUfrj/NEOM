"""
    Code Protocols
    Author: Amanda
"""
__all__ = ['MessageHandler',
           'createUserFile',
           'UserAuthentication']


# Onde colocar tratamento de caracteres especiais??

class MessageHandler:
    def __init__(self):
        """
            Protocol to Handle Message Transmitions.
        """
        self.cleanAll()

    def cleanAll(self):
        self.text = ""
        self.picture = None
        self.document = None
        self.other = []
        self.authentication = None

    def addMessage(self, text):
        import base64
        self.text = base64.b64encode(text)

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

    def addAuthentication(self, user, password):
        self.authentication = [user, password]

    def sendMessage(self):
        import json
        attrDict = {
                        'text': self.text,
                        'other': self.other,
                        'picture': self.picture,
                        'document': self.document,
                        'authentication': self.authentication
                    }
        return json.dumps(attrDict)

    def receiveMessage(self, binary):
        self.cleanAll()
        import json
        attrDict = json.loads(binary)
        self.text = attrDict[u'text']
        self.other = attrDict[u'other']
        self.picture = attrDict[u'picture']
        self.document = attrDict[u'document']
        self.authentication = attrDict[u'authentication']

    def sendAuthentication(self, user, password, new=False, remove=False):
        self.addOther("authenticate")
        # out.addMessage("UserAuthentication")
        if new:
            self.addOther("add")
            if remove: raise Warning("Cannot add and remove user at the same time. Only adding instead.")
        elif remove:
            self.addOther("rm")
        self.addAuthentication(user, password)
        return self.sendMessage()

    def readMessage(self):
        if len(self.text) == 0: return None
        return self.text.decode('base64')

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
        if len(self.other) == 0: return None
        return self.other

    def readAuthentication(self):
        if not self.authentication: return None
        return {'user': self.authentication[0],
                'password': self.authentication[1]}


def createUserFile(name, service, path=".", sufix="pic.tz", algorithm="md5"):
    # TODO: Make file that can only be edited through the code
    if algorithm not in ['sha1', 'sha224', 'sha384', 'sha256', 'sha512', 'md5']:
        raise NotImplementedError('Hash function "%s" not found' % (algorithm))
    filename = "%s/%s.%s"%(path, name, sufix)
    file = open(filename, 'w')
    lines = ["USERS FOR %s SERVER"%(service.upper()), "\n",
             "Hash algorithm: %s"%(algorithm), "\n"
             "\n",
             "-"*20, "\n"]
    file.writelines(lines)
    file.close()
    return filename


class UserAuthentication:
    def __init__(self, usersFile):
        """
            Protocol to authenticate users of a system.
            :param usersFile: path of file with list of users (created with function createUserFile)
        """
        self.file = usersFile
        file = open(self.file, 'r')
        line = file.readlines()[1]
        if line.split(":")[0] != "Hash algorithm":
            raise TypeError("File %s not within prescriptions."%(usersFile))
        self.algorithm = line.split(" ")[-1][:-1]
        file.close()

    def _getHash(self, text):
        import hashlib
        if self.algorithm == "md5":
            return hashlib.md5(text).hexdigest()
        elif self.algorithm == "sha1":
            return hashlib.sha1(text).hexdigest()
        elif self.algorithm == "sha224":
            return hashlib.sha224(text).hexdigest()
        elif self.algorithm == 'sha384':
            return hashlib.sha384(text).hexdigest()
        elif self.algorithm == 'sha256':
            return hashlib.sha256(text).hexdigest()
        elif self.algorithm == 'sha512':
            return hashlib.sha512(text).hexdigest()

    def addUser(self, user, password):
        # TODO: Save users in alphabetic order
        passHash = self._getHash(password)
        file = open(self.file, 'r+')
        lines = file.readlines()
        for line in lines[4:]:
            if line.split(',')[0] == user:
                raise NameError("There is already a user with this name")
        text = "%s,%s\n"%(user, passHash)
        file.write(text)
        file.close()

    def checkUser(self, user, password):
        passHash = self._getHash(password)
        file = open(self.file, 'r')
        lines = file.readlines()
        file.close()
        for line in lines[4:]:
            words = line.split(',')
            if words[0] == user:
                if passHash == words[1]:
                    return "User verified"
                else:
                    return "Wrong Password"
        return "No user"

    def rmUser(self, user, password):
        passHash = self._getHash(password)
        file = open(self.file, 'r+')
        lines = file.readlines()
        for line in lines[4:]:
            words = line.split(',')
            if words[0] == user:
                if passHash == words[1]:
                    lines.remove(line)
                    file.close()
                    file = open(self.file, 'w')
                    file.writelines(lines)
                    file.close()
                    return "User removed"
                else:
                    file.close()
                    return "Wrong Password"
        file.close()
        return "No user"
