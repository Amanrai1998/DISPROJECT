import socket


class RegistrationService:
    def __init__(self, s: socket.socket, kdcIP: str, kdcPort: int, nodeType: str, buffSize: int):
        self.s = s
        self.kdcIP = kdcIP
        self.kdcPort = kdcPort
        self.nodeType = nodeType
        self.buffSize = buffSize

    def register(self):
        message = 'Register,' + self.nodeType
        self.s.sendto(message.encode(), (self.kdcIP, self.kdcPort))
        data, addr = self.s.recvfrom(self.buffSize)
        print(data.decode())
        print(addr)
        print("Registration Successful")
