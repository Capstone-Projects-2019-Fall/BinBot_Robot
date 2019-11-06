# Author: Sean DiGirolamo
# Date: 10/30/2019
import select
import socket


JAVA_INT_BYTES = 4
ACK = b'\x01'
ACK_BYTES = 1
ENDIAN = "big"


class Connection:
    def __init__(self, ip, port):
        self.__ip = ip
        self.__port = port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setblocking(True)
        self.__sock.connect((ip, port))

    def send(self, msg):
        print("SENDING MESSAGE " + msg)
        self.__sock.sendall(str.encode(msg + "\n"))
        self.__receive_ack()
        print()

    def receive(self):
        print("RECEIVING")

        length = self.__receive_length()

        retval = self.__sock.recv(length).decode("utf-8")
        print("RECEIVED " + retval)

        self.__send_ack()
        self.__drain()

        print()

        return retval

    def __receive_length(self):
        print("Waiting for length")
        retval = int.from_bytes(self.__sock.recv(JAVA_INT_BYTES), ENDIAN)
        print("Received length: " + str(retval))
        self.__send_ack()
        return retval

    def __send_ack(self):
        print("Sending ACK")
        self.__sock.sendall(ACK)
        self.__sock.sendall(str.encode("\n"))

    def __receive_ack(self):
        print("Waiting for ACK")
        data = self.__sock.recv(ACK_BYTES)
        print("Received ACK: " + str(data))

    def __drain(self):
        """remove the data present on the socket"""
        input = [self.__sock]
        while 1:
            inputready, o, e = select.select(input, [], [], 0.0)
            if len(inputready) == 0: break
            for s in inputready: s.recv(1)
