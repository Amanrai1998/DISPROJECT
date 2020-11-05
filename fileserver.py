#!/usr/bin/env python

import sys
import socket

def registration():
    #check in db if server with ip exist

    #if fsi or dsi

    #generate a Unique Symmentric Key And ID
    #add db entry ID, IP, PORT, Nodetype, symmetric key, FILES, Session Key with expiry(empty)

    #Send Registration Confirmation
    print("Registration Function")

UDP_IP = '127.0.0.1'
UDP_PORT = int(sys.argv[1])
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((UDP_IP, UDP_PORT))

#Registration Request
s.sendto("Register F", ('127.0.0.1', 2000))
