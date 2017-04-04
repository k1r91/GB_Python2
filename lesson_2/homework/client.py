__author__ = "Kirill Cherkasov"
# Клиент игры "Запоминалка"

import socket
import datetime

from transaction import *


class PaymentTerminal:

    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port

    def execute(self, transaction):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        sock.sendall(transaction.serialize())
        recvd = str(sock.recv(1024), 'utf-8')
        print(recvd)
        sock.close()


def main():
    if __name__ == '__main__':
        transaction_pool = [PaymentTransaction((25, 1000)),
                            PaymentTransaction((32, 2000)),
                            PaymentTransaction((25, 5000)),
                            PaymentTransaction((42, 2000)),
                            EncashmentTransaction((1, 1000))]
        terminal = PaymentTerminal()
        for transaction in transaction_pool:
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
