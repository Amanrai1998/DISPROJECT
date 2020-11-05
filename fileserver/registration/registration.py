import socket


class RegistrationService:
    def __init__(self, s: socket, kdcIP: str, kdcPort: int, nodeType: str):
        self.s = s
        self.kdcIP = kdcIP
        self.kdcPort = kdcPort
        self.nodeType = nodeType

    def register(self):
        message = 'Register,' + self.nodeType
        self.s.sendto(message.encode(), (self.kdcIP, self.kdcPort))
        print("Registration Successful")
