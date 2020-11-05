import socket


class RegistrationService:
    def __init__(self, s: socket.socket, kdcIP: str, kdcPort: int, nodeType: str, buffSize: int):
        self.s = s
        self.kdcIP = kdcIP
        self.kdcPort = kdcPort
        self.nodeType = nodeType
        self.buffSize = buffSize

    async def register(self):
        message = 'Register,' + self.nodeType
        await self.s.sendto(message.encode(), (self.kdcIP, self.kdcPort))
        data, addr = await self.s.recvfrom(self.buffSize)
        print("Registration Successful")
        return {data, addr}
