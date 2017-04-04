__author__ = "Kirill Cherkasov"
# Сервер игры "Запоминалка"

import socketserver
from transaction import Transaction


class MemTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).decode()
        # print("Клиент {} сообщает {}".format(self.client_address[0], self.data))
        transaction = Transaction.deserialize(self.data)
        if transaction:
            log = "Received from {} {} at {}".format(self.client_address[0],
                                           transaction,
                                            transaction.time)

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

          
HOST, PORT = 'localhost', 9999

server = socketserver.TCPServer((HOST, PORT), MemTCPHandler)  
print('Сервер запущен')

server.serve_forever()
server.server_close()

