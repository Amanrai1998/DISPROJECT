import socket
import asyncio
import secrets
from cryptography.fernet import Fernet

# GLOBALS


class User:
    def __init__(self, ID, addr, nType, SK, Files):
        self.ID = ID
        self.addr = addr
        self.nType = nType
        self.SK = SK
        self.Files = Files


class DB:  # DATABASE
    Users = []

    def __init__(self):
        print("DB Connected")

    def findUser(self, ID):
        for user in self.Users:
            if(user.ID==ID):
                return user
        return None

    def findUserByAddr(self, addr):
        for user in self.Users:
            if(user.addr == addr):  # check addr structure
                return user
        return None

    def registerUser(self, addr, nType):
        # generate a Unique Symmentric Key And ID
        ID = secrets.token_hex(14)  # Check Uniqueness
        SK = Fernet.generate_key()
        # add db entry ID, IP, PORT, Nodetype, symmetric key, FILES, Session Key with expiry(empty)
        user = User(ID, addr, nType, SK, [])
        self.Users.append(user)

        return user

    def registerFile(self, ID, file):
        for user in self.Users:
            if(user.ID == ID):  # check addr structure
                return user.Files.append(file)
        return None


UDP_IP = '127.0.0.1'
UDP_PORT = 2000
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((UDP_IP, UDP_PORT))

db = DB()

# Request Functions


async def registration(addr, data):
    # check in db if server with ip exist
    user = db.findUserByAddr(addr)

    if(user != None):
        message = "Already Registered"
        s.sendto(message.encode(), addr)
        return

    # register user
    user = db.registerUser(addr, data[1])

    # Send Registration Confirmation
    message = "Registered,"+user.ID+","+user.SK.decode()
    s.sendto(message.encode(), addr)
    print("Registered")


async def authentication(addr, data):
    # find user in db
    sourceUser = db.findUser(data[2])
    destinationUser = db.findUser(data[3])
    # user null check
    # Send Encrypted Message
    sessionKey = Fernet.generate_key()
    # encryption for destination
    f = Fernet(destinationUser.SK)
    destinationEncrption = f.encrypt((str(data[2])+","+sessionKey.decode()).encode())
    # encryption for source
    f = Fernet(sourceUser.SK)
    sourceEncryption = f.encrypt(
        (data[1]+","+data[3]+","+sessionKey.decode()+","+destinationEncrption.decode()).encode()
    )
    message = "Authenticated,"+sourceEncryption.decode()
    s.sendto(message.encode(), addr)

async def lookup(addr, data):
    #find user by addr in db
    user = db.findUserByAddr((data[1], int(data[2])))

    message = "Lookup,"+user.ID
    s.sendto(message.encode(), addr)

async def fileRegisteration(addr, data):
    #find user in db
    user = db.findUser(data[1])

    #update files array in db
    user = db.registerFile(data[2])

    message = "File Registered"
    s.sendto(message.encode(), addr)
    #send new file info to every node

# main

async def main():
    while(1):
        data, addr = s.recvfrom(BUFFER_SIZE)

        data = data.decode()

        data = data.split(',')

        if(data[0] == "Register"):
            # Registration Module
            # task = asyncio.create_task(registration(addr, data))
            await registration(addr, data)
            # task
        elif(data[0] == "Authenticate"):
            # Authentication Module
            await authentication(addr, data)
        elif(data[0] == "Lookup"):
            #Look up
            await lookup(addr, data)
        elif(data[0] == "File Registration"):
            await fileRegisteration(addr, data)


# Run KDC
if __name__ == '__main__':
    asyncio.run(main())
