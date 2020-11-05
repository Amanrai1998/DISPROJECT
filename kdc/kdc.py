#!/usr/bin/env python

import socket
import secrets

#GLOBALS
class User:
    def __init__(self, ID, IP, PORT, nType, SK, Files, sessionKey):
        self.ID = ID
        self.IP = IP
        self.PORT = PORT
        self.nType = nType
        self.SK = SK
        self.Files = Files
        self.sessionKey = sessionKey


class DB:   #DATABASE
    User = []

    def __init__(self):
        print("DB Connected")

    def findUserByAddr(self, addr):
        for user in self.USER:
            if(user.IP == addr.UDP_IP and user.PORT == addr.UDP_PORT):
                return user
        return None

    def registerUser(self, addr, nType):
        #generate a Unique Symmentric Key And ID
        ID = secrets.token_hex(14)  #Check Uniqueness
        SK = secrets.token_hex(32)
        #add db entry ID, IP, PORT, Nodetype, symmetric key, FILES, Session Key with expiry(empty)
        user = User(ID,addr.UDP_IP,addr.UDP_PORT,nType,SK,[],None)
        self.User.append(user)

        return user

UDP_IP = '127.0.0.1'
UDP_PORT = 2000
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((UDP_IP, UDP_PORT))

db = DB()

async def registration(addr, data):
    #check in db if server with ip exist
    user = db.findUserByAddr(addr)

    if(user != None):
        message = "AlreadyRegistered"
        s.sendto(message, (addr.UDP_IP, addr.UDP_PORT))
        return

    #register user
    user = db.registerUser(addr, data[1])

    #Send Registration Confirmation
    message = "Registered "+user.ID+" "+user.SK
    s.sendto(message, (addr.UDP_IP, addr.UDP_PORT))

data,addr = s.recvfrom(BUFFER_SIZE)

data = data.split(' ')

if(data[0]=="Register"):
    #Registration Module
    registration(addr, data)