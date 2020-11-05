#!/usr/bin/env python

import socket

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

db = DB()

async def registration(s, addr, data):
    #check in db if server with ip exist
    user = db.findUserByAddr(addr)

    if(user != None):
        print("Node Already Registered")
        return

    #if fsi or dsi

    #generate a Unique Symmentric Key And ID
    #add db entry ID, IP, PORT, Nodetype, symmetric key, FILES, Session Key with expiry(empty)

    #Send Registration Confirmation
    print("Registration Function")

UDP_IP = '127.0.0.1'
UDP_PORT = 2000
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((UDP_IP, UDP_PORT))

data,addr = s.recvfrom(BUFFER_SIZE)

data = data.split(' ')

if(data[0]=="Register"):
    #Registration Module
    registration(s, addr, data)