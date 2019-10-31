# Author: Sean DiGirolamo
# Date: 10/30/2019
import socket


JAVA_INT_BYTES = 4
ENDIAN = "big"


class Connection:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

    def send(self, msg):
        self.sock.sendall(str.encode(msg + "\n"))
        return self.sock.recv(JAVA_INT_BYTES)

    def receive(self):
        length = int.from_bytes(self.sock.recv(JAVA_INT_BYTES), ENDIAN)
        print("LENGTH: " + str(length))
        retval = str(self.sock.recv(length))
        retval = retval[retval.find('{'):]
        return retval.rsplit('}', 1)[0] + '}'
