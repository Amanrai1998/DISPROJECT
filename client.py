#!/usr/bin/env python3

import sys
import asyncio
import socket
import time
import random
from cryptography.fernet import Fernet

from registration.registration import RegistrationService
# from registration.registration import RegistrationService

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


async def authenticate(s, PORT):
    destId = lookup(s, PORT)
    if(destId == None):
        print("Authentication Error")
        return

    PORT = int(PORT)

    # send to KDC
    nonce1 = random.randint(0, 100)
    message = "Authenticate,"+str(nonce1)+","+ID+","+destId
    s.sendto(message.encode(), (KDC_IP, KDC_SERVER_PORT))

    # Recieve from KDC
    data, addr = s.recvfrom(BUFFER_SIZE)
    data = data.decode()
    data = data.split(',')
    if(data[0] != "Authenticated"):
        print("Authentication Error")
        return

    # nonce matching
    f = Fernet(SK)
    decodedData = f.decrypt(data[1].encode())
    decodedData = decodedData.decode()
    decodedData = decodedData.split(',')
    if(nonce1 != int(decodedData[0])):
        print("Nonce Match Error")
        return

    # Send to File server
    nonce2 = random.randint(0, 100)
    sessKey = decodedData[2].encode()
    f = Fernet(sessKey)
    encryptedNonce2 = f.encrypt(str(nonce2).encode())
    message = "Authenticate,"+encryptedNonce2.decode()+","+decodedData[3]
    s.sendto(message.encode(), ('127.0.0.1', PORT))

    # Recieve from file server
    data, addr = s.recvfrom(BUFFER_SIZE)
    data = data.decode()
    data = data.split(',')
    if(data[0] != "Authenticate"):
        print("Authentication Error")
        return

    # nonce matching
    decodedData = f.decrypt(data[1].encode())
    decodedData = decodedData.decode()
    decodedData = decodedData.split(',')
    if(nonce2-1 != int(decodedData[0])):
        print("Nonce Match Error")
        return

    # Send to file server for verification
    encryptedDestNonce = f.encrypt(str(int(decodedData[1])-1).encode())
    message = "Authenticated,"+encryptedDestNonce.decode()
    s.sendto(message.encode(), ('127.0.0.1', PORT))

    # Recieve from file server authenticated
    data, addr = s.recvfrom(BUFFER_SIZE)
    data = data.decode()
    data = data.split(',')
    if(data[0] != "Authenticated"):
        print("Authentication Error")
        return

    global sessionKey
    sessionKey = sessKey


def lookup(s, PORT):
    message = 'Lookup,127.0.0.1,'+PORT
    s.sendto(message.encode(), (KDC_IP, KDC_SERVER_PORT))
    data, addr = s.recvfrom(BUFFER_SIZE)
    data = data.decode()
    data = data.split(',')
    if(data[0] == "Lookup"):
        return data[1]
    return None


async def callRPC(s, msg, port):
    s.sendto(msg, (UDP_IP, int(port)))
    data, addr = s.recvfrom(BUFFER_SIZE)
    return data.decode()


async def main():
    print('Client Started')

    # Start socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the server to port
    server_socket.bind((UDP_IP, UDP_PORT))

    # Instantiate the registration service
    registrationService = RegistrationService(
        server_socket, KDC_IP, KDC_SERVER_PORT, 'D', BUFFER_SIZE)

    # Register server with KDC
    data, addr = await registrationService.register()

    if(data[0] == 'Registered'):
        global ID
        global SK
        ID = data[1]
        SK = data[2].encode()

    while(True):
        inp = input()
        inp = inp.split(',')

        await authenticate(server_socket, inp[len(inp) - 1])
        msg: str = inp[0]
        f = Fernet(sessionKey)
        output = await callRPC(server_socket, f.encrypt(msg.encode()), inp[len(inp) - 1])
        print(output)

        # if(inp[0] == "Authenticate"):
        #     await authenticate(server_socket, inp[1])
        # if(inp[0] == "RPC"):
        #     if(sessionKey is None or sessionKey == ''):
        #         print('Not Authenticated')
        #     else:
        #         msg: str = inp[0] + ',' + inp[1]
        #         f = Fernet(sessionKey)
        #         output = await callRPC(server_socket, f.encrypt(msg.encode()), inp[2])
        #         print(output)


if __name__ == "__main__":
    asyncio.run(main())
