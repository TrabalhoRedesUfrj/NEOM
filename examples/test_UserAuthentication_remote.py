"""
    Test of User Authentication Protocol
    Creating Enviroment to Authenticate Users
    Author: Amanda
"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))

from Protocol import MessageHandler, createUserFile, UserAuthentication

# Configuration of UserAuthentication object
# -------------------------------------------
name = 'userfile_test'
server = 'neom'
filename = createUserFile(name,server)
manager = UserAuthentication(filename)
users = [["user1","minhasenha"],
         ["user2","minhasenha2"]]
for user, senha in users:
    try:
        manager.addUser(user,senha)
    except NameError:
        pass
# -------------------------------------------


# Client request: New user
# -------------------------------------------
comm = "Create new user" # "Remove user" or None
user = "meunome"
senha = "ehzoado"
print "%s:\n\tUser '%s'\n\tPassword '%s'"%(comm,user,senha)
# inputs from client

if comm == "Create new user":
    new, rm = True, False
elif comm == "Remove user":
    new, rm = False, True
else:
    new, rm = False, False
client = MessageHandler()
message = client.sendAuthentication(user, senha, new=new, remove=rm)
# -------------------------------------------


# Server receives message
# -------------------------------------------
server = MessageHandler()
server.receiveMessage(message)
commands = server.readOther()
if "authenticate" in commands:
    out = MessageHandler()
    out.addOther("authenticate")
    auth = server.readAuthentication()
    if "add" in commands:
        try:
            manager.addUser(auth['user'], auth['password'])
            out.addOther("ok")
        except NameError:
            out.addOther("fail")
            out.addMessage("User already used. Choose another.")
    elif "rm" in commands:
        text = manager.rmUser(user,senha)
        if text == "User removed": out.addOther("ok")
        else:
            out.addOther("fail")
            if text == "Wrong Password": out.addMessage("%s. Try again."%(text))
            elif text == "No user": out.addMessage("%s found. Try again."%(text))
    else:
        text = manager.checkUser()
        if text == "User verified": out.addOther("ok")
        else:
            out.addOther("fail")
            if text == "Wrong Password": out.addMessage("%s. Try again."%(text))
            elif text == "No user": out.addMessage("%s found. Try again."%(text))
    response = out.sendMessage()
else:
    raise NotImplementedError("User has not been authenticated since no authentication data has been given")
# -------------------------------------------


# Client receives response
# -------------------------------------------
client.cleanAll()
client.receiveMessage(response)
commands = client.readOther()
if "authenticate" in commands:
    if "ok" in commands:
        print "'%s' command executed correctly."%(comm)
    elif "fail" in commands:
        text = client.readMessage()
        print "Could not execute '%s'command:\n%s"%(comm,text)
    else:
        print "Error: Response could not be interpreted."
else:
    print "Error: No response given."
# -------------------------------------------


# Finalizing
# -------------------------------------------
file = open(filename)
lines = file.readlines()
file.close()
os.remove(filename)
print ("_"*40)
for line in lines:
    print line[:-1]
# -------------------------------------------