#!/usr/bin/env python3

import sys
import asyncio
import socket
import time
import random
from cryptography.fernet import Fernet

from registration.registration import RegistrationService

# Global Constants
UDP_IP = '127.0.0.1'
UDP_PORT = int(sys.argv[1])
BUFFER_SIZE = 1024
KDC_SERVER_PORT = 2000
KDC_IP = '127.0.0.1'

# Will be generated after registation
ID = ''
SK = ''
sessionKey = ''

def authenticate(s, PORT):
    destId = lookup(s, PORT)
    if(destId == None):
        print("Authentication Error")
        return

    nonce1 = random.randint(0, 100)
    message = "Authenticate,"+nonce1+","+ID+","+destId
    s.sendto(message.encode(), (KDC_IP, KDC_SERVER_PORT))

    data, addr = s.recvfrom(BUFFER_SIZE)
    data = data.split(',')
    if(data[0] != "Authenticated"):
        print("Authentication Error")
        return
    
    f = Fernet(SK)
    decodedData = f.decrypt(data[1])
    decodedData = decodedData.split(',')
    if(nonce1 != int(decodedData[0])):
        print("Nonce Match Error")
        return

    nonce2 = random.randint(0, 100)
    sessKey = decodedData[2].encode()
    f = Fernet(decodedData[2].encode())
    encryptedNonce2 = f.encrypt(""+nonce2)
    message = "Authenticate,"+encryptedNonce2+","+decodedData[3]
    s.sendto(message.encode(), ('127.0.0.1', PORT))

    data, addr = s.recvfrom(BUFFER_SIZE)

    data = data.split(',')
    if(data[0] != "Authenticate"):
        print("Authentication Error")
        return
    
    decodedData = f.decrypt(data[1])
    decodedData = decodedData.split(',')
    if(nonce2-1 != int(decodedData[0])):
        print("Nonce Match Error")
        return

    encryptedDestNonce = f.encrypt(int(decodedData[1])-1)
    message = "Authenticated,"+encryptedDestNonce
    s.sendto(message.encode(), ('127.0.0.1', PORT))

    data, addr = s.recvfrom(BUFFER_SIZE)
    data = data.split(',')
    if(data[0] != "Authenticated"):
        print("Authentication Error")
        return
    
    global sessionKey
    sessionKey = sessKey
    print("Authenticated")


async def main():
    print('Server Started')

    # Start socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the server to port
    server_socket.bind((UDP_IP, UDP_PORT))

    # Instantiate the registration service
    registrationService = RegistrationService(
        server_socket, KDC_IP, KDC_SERVER_PORT, 'F', BUFFER_SIZE)

    # Register server with KDC
    credentials = await registrationService.register()

    while(True):
        time.sleep(10)
        print('listning...')


if __name__ == "__main__":
    asyncio.run(main())
