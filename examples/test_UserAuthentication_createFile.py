"""
    Test of User Authentication Protocol
    Creating file within specifications and adding users to it
    Author: Amanda
"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))

from Protocol import createUserFile, UserAuthentication
name = 'userfile_test'
server = 'neom'

filename = createUserFile(name,server)

manager = UserAuthentication(filename)
senhas = [["eu","minhasenha"],
          ["me","minhasenha2"],
          ["eu","minhasenha3"]]

for senha in senhas:
    print "Adding user %s" % (senha[0])
    try:
        manager.addUser(senha[0],senha[1])
    except NameError:
        print "Name '%s' already used. Try another username."%(senha[0])

file = open(filename)
lines = file.readlines()
file.close()
os.remove(filename)

print ("_"*40)+"\nFile:"
for line in lines:
    print line[:-1]