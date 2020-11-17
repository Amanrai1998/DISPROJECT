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
sessionKey = {}

def authenticate(s, addr, data):
    #decode recived data destNonce, (SourceId, sessionKey)
    f = Fernet(SK)
    decodedData = f.decrypt(data[2].encode())
    decodedData = decodedData.decode()
    decodedData = decodedData.split(',')
    sourceId = decodedData[0]
    sessionKey[sourceId] = decodedData[1].encode()

    f = Fernet(sessionKey[sourceId])
    recNonce = int(f.decrypt(data[1].encode()))

    #send to node updated nonce and server nonce
    nonce1 = random.randint(0, 100)
    encryptedData = f.encrypt((str(recNonce-1)+","+str(nonce1)).encode())
    message = "Authenticate,"+encryptedData.decode()
    s.sendto(message.encode(), addr)

    #recieve from node
    data, addr = s.recvfrom(BUFFER_SIZE)
    data = data.decode()
    data = data.split(',')
    if(data[0] != "Authenticated"):
        print("Authentication Error")
        return
    
    #decode sent note to verify
    decodedData = f.decrypt(data[1].encode())
    decodedData = decodedData.decode()
    decodedData = decodedData.split(',')
    if(nonce1-1 != int(decodedData[0])):
        print("Nonce Match Error")
        return

    #send to node success
    message = "Authenticated"
    s.sendto(message.encode(), addr)

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
    data, addr = await registrationService.register()

    if(data[0]=='Registered'):
        global ID
        global SK
        ID = data[1]
        SK = data[2].encode()

    while(True):
        data, addr = server_socket.recvfrom(BUFFER_SIZE)

        data = data.decode()

        data = data.split(',')

        if(data[0]=='Authenticate'):
            authenticate(server_socket, addr, data)

        # time.sleep(10)
        # print('listning...')


if __name__ == "__main__":
    asyncio.run(main())
