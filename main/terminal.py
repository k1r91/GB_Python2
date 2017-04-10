import socket

from transaction import *


class PaymentTerminal:

    def __init__(self, id, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.id = id
        self.transaction_id = 0

    def execute(self, transaction):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        sock.sendall(transaction.serialize())
        recvd = str(sock.recv(1024), 'utf-8')
        print(recvd)
        sock.close()

    def make_payment_transaction(self, data):
        self.transaction_id += 1
        return PaymentTransaction(self.id, self.transaction_id, data)

    def make_encashment(self, data):
        self.transaction_id += 1
        return EncashmentTransaction(self.id, self.transaction_id,data)

    def make_service_request(self, data):
        self.transaction_id += 1
        return ServiceTransaction(self.id, self.transaction_id, data)