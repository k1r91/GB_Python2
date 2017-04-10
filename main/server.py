__author__ = "Kirill Cherkasov"
# Сервер игры "Запоминалка"

import socketserver

from main.transaction import Transaction

socketserver.TCPServer.allow_reuse_address = True


class MemTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024)
        print("Клиент {} сообщает {}".format(self.client_address[0], self.data))
        transaction = Transaction.deserialize(self.data)
        if transaction:
            log = "Received from {} {} {}".format(self.client_address[0],
                                           transaction, transaction.time)

            # обработка транзакции
            self.process(transaction)
            # записываем лог
            self.write(log)
            # посылаем ответ
            self.request.sendall(bytes('OK', 'utf-8'))
        else:
           print("Unknown request")

    def write(self, data):
        print(data)

    def process(self, transaction):
        pass


class Server:

    def __init__(self, host='localhost', port=9999):
        self.host, self.port = host, port

    def serve(self):
        server = socketserver.TCPServer((self.host, self.port), MemTCPHandler)
        print("Сервер запущен")
        server.serve_forever()


def main():
    server = Server()
    server.serve()

if __name__ == '__main__':
    main()