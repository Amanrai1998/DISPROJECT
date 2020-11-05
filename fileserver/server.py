#!/usr/bin/env python3

import sys
import socket
from registration.registration import RegistrationService

# Registration Request

UDP_IP = '127.0.0.1'
UDP_PORT = int(sys.argv[1])
BUFFER_SIZE = 1024
KDC_SERVER_PORT = 2000
KDC_IP = '127.0.0.1'


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((UDP_IP, UDP_PORT))
    print(socket.gethostbyname(KDC_URL))
    registrationService = RegistrationService(
        server_socket, KDC_IP, KDC_SERVER_PORT, 'F')
    registrationService.register()
    print('hello world')


if __name__ == "__main__":
    main()
