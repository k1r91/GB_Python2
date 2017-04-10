__author__ = "Kirill Cherkasov"
# Клиент игры "Запоминалка"

import socket

from terminal import PaymentTerminal


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
