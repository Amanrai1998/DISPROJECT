import socket


class RegistrationService:
    def __init__(self, s: socket, kdcPort: int, nodeType: str):
        self.s = s
        self.kdcPort = kdcPort
        self.nodeType = nodeType

    def register(self):
        message = 'Register,' + self.nodeType
        self.s.sendto(message.encode(), ('127.0.0.1', 2000))
        print("Registration Successful")
