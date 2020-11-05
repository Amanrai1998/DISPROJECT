#!/usr/bin/env python3

import sys
import socket
from registration.registration import RegistrationService

# Registration Request

UDP_IP = '127.0.0.1'
UDP_PORT = int(sys.argv[1])
BUFFER_SIZE = 1024
KDC_SERVER_PORT = 2000


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((UDP_IP, UDP_PORT))
    registrationService = RegistrationService(s, KDC_SERVER_PORT, 'F')
    registrationService.register()
    print('hello world')


if __name__ == "__main__":
    main()
