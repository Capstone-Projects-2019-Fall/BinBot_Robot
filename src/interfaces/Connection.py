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
        print("SENDING MESSAGE " + msg)
        self.sock.sendall(str.encode(msg + "\n"))
        print("WAITING FOR ACK")
        ack = self.sock.recv(JAVA_INT_BYTES)
        print("RECIEVED ACK " + str(int.from_bytes(ack, ENDIAN)))
        print()

    def receive(self):
        print("RECEIVING")
        length = int.from_bytes(self.sock.recv(JAVA_INT_BYTES), ENDIAN)
        print("LENGTH: " + str(length))
        retval = str(self.sock.recv(length))
        retval = retval[retval.find('{'):]
        retval = retval.rsplit('}', 1)[0] + '}'
        print("RECEIVED " + retval)
        print("SENDING ACK " + str(1))
        self.sock.sendall((1).to_bytes(4, ENDIAN))
        print()
        return retval
