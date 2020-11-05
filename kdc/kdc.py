import socket
import secrets
from cryptography.fernet import Fernet

#GLOBALS
class User:
    def __init__(self, ID, IP, PORT, nType, SK, Files):
        self.ID = ID
        self.IP = IP
        self.PORT = PORT
        self.nType = nType
        self.SK = SK
        self.Files = Files


class DB:   #DATABASE
    User = []

    def __init__(self):
        print("DB Connected")

    def findUserByAddr(self, addr):
        for user in self.USER:
            if(user.IP == addr.UDP_IP and user.PORT == addr.UDP_PORT): #check addr structure
                return user
        return None

    def registerUser(self, addr, nType):
        #generate a Unique Symmentric Key And ID
        ID = secrets.token_hex(14)  #Check Uniqueness
        SK = Fernet.generate_key()
        print(SK)
        #add db entry ID, IP, PORT, Nodetype, symmetric key, FILES, Session Key with expiry(empty)
        user = User(ID,addr.UDP_IP,addr.UDP_PORT,nType,SK,[])
        self.User.append(user)

        return user

UDP_IP = '127.0.0.1'
UDP_PORT = 2000
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((UDP_IP, UDP_PORT))

db = DB()

#Request Functions
async def registration(addr, data):
    #check in db if server with ip exist
    user = db.findUserByAddr(addr)

    if(user != None):
        message = "Already Registered"
        s.sendto(message, (addr.UDP_IP, addr.UDP_PORT))
        return

    #register user
    user = db.registerUser(addr, data[1])

    #Send Registration Confirmation
    message = "Registered,"+user.ID+","+user.SK
    s.sendto(message, (addr.UDP_IP, addr.UDP_PORT))

async def authentication(addr, data):
    #find user in db
    sourceUser = db.findUser(data[2])
    destinationUser = db.findUser(data[3])
    #user null check
    #Send Encrypted Message
    sessionKey = Fernet.generate_key()
    #encryption for destination
    f = Fernet(destinationUser.SK)
    destinationEncrption = f.encrypt(data[2]+","+sessionKey)
    #encryption for source
    f = Fernet(sourceUser.SK)
    sourceEncryption = f.encrypt(data[1]+","+data[3]+","+sessionKey+","+destinationEncrption)
    message = "Authenticated,"+sourceEncryption
    s.sendto(message, (addr.UDP_IP, UDP_PORT))

#main
def main():
    data,addr = s.recvfrom(BUFFER_SIZE)

    data = data.split(',')

    if(data[0]=="Register"):
        #Registration Module
        registration(addr, data)
    elif(data[0]=="Authenticate"):
        #Authentication Module
        authentication(addr, data)


#Run KDC
main()

