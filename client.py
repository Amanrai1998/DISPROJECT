#!/usr/bin/env python3

import sys
import socket
import time

from registration.registration import RegistrationService
# from registration.registration import RegistrationService

# Global Constants
UDP_IP = '127.0.0.1'
UDP_PORT = int(sys.argv[1])
BUFFER_SIZE = 1024
KDC_SERVER_PORT = 2000
KDC_IP = '127.0.0.1'


def main():
    print('Server Started')

    # Start socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the server to port
    server_socket.bind((UDP_IP, UDP_PORT))

    # Instantiate the registration service
    registrationService = RegistrationService(
        server_socket, KDC_IP, KDC_SERVER_PORT, 'D', BUFFER_SIZE)

    # Register server with KDC
    registrationService.register()

    while(True):
        time.sleep(10)
        print('Waiting...')


if __name__ == "__main__":
    main()
