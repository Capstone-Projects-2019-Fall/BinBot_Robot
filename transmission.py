# Author: Sean DiGirolamo
# Date: 10/30/2019
import socket


class Connection:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

    def send(self, msg):
        self.sock.sendall(msg)

    def receive(self):
        self.sock.recv()
