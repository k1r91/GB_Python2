__author__ = "Kirill Cherkasov"
# Клиент игры "Запоминалка"

import socket
import datetime

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

def main():
    if __name__ == '__main__':
        terminal = PaymentTerminal(324)
        pool = [
            terminal.make_payment_transaction((4, 10)),
            terminal.make_payment_transaction((24, 1023)),
            terminal.make_payment_transaction((32, 2048)),
            terminal.make_service_request('reload'),
            terminal.make_encashment((25, 1000))
        ]
        for transaction in pool:
            terminal.execute(transaction)

main()

'''print('Клиент запущен')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

sock.sendall(bytes('I_WANNA_PLAY', 'utf-8'))

recvd = str(sock.recv(1024), 'utf-8')

#sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

sock.sendall(bytes('I_WANNA_PLAZ', 'utf-8'))

recvd2 = str(sock.recv(1024), 'utf-8')

print(recvd)
print(recvd2)

sock.close()'''
