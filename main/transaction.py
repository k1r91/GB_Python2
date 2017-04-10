__author__ = "Kirill Cherkasov"

import sys
import struct
import binascii
import math

from datetime import datetime


class Transaction:
    '''
    реализация протокола
    '''

    MAX_AMOUNT = 18446744073709551614  # 8 байт
    MAX_ID = 4294967295   # 4 байта

    TRANSACTION_TYPES = ['service', 'payment', 'encashment']

    def __init__(self, terminal_id, transaction_id, t_type, data, t_time=None):
        self.header = '0111101001111010'  # 'zz'
        self.t_type = t_type
        self.data = data
        self.validate_type()
        self.terminal_id = terminal_id
        self.transaction_id = transaction_id
        if t_time:
            self.t_time = t_time
        else:
            self.t_time = self.get_time()

    def validate_type(self):
        if self.t_type not in Transaction.TRANSACTION_TYPES:
            raise TransactionTypeException(self)

    @staticmethod
    def get_time():
        year = datetime.today().year
        month = datetime.today().month
        day = datetime.today().day
        year = bin(year - 2000)[2:].zfill(7)
        month = bin(month)[2:].zfill(4)
        day = bin(day)[2:].zfill(5)
        now = datetime.now()
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        seconds = (now - midnight).seconds
        seconds = bin(seconds)[2:].zfill(24)
        result = "".join((year, month, day, seconds))
        return result

    @property
    def time(self):
        year = self.t_time[:7]
        year = int(year, 2) + 2000
        month = int(self.t_time[7:11], 2)
        day = int(self.t_time[11:16], 2)
        seconds = int(self.t_time[16:], 2)
        hours = seconds // 3600
        minutes = (seconds - hours * 3600) // 60
        seconds = seconds - hours * 3600 - minutes * 60
        result = "{:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(year, month, day,
                                                                    hours, minutes, seconds)
        return result

    @property
    def base_serialize(self):
        transaction_id = bin(self.transaction_id)[2:].zfill(64)
        terminal_id = bin(self.terminal_id)[2:].zfill(32)
        transaction_type = bin(self.TRANSACTION_TYPES.index(self.t_type))[2:].zfill(2)
        return "".join((self.t_time, transaction_id, terminal_id, transaction_type))

    def serialize(self):
        partner_id = bin(self.data[0])[2:].zfill(32)
        transaction_amount = bin(self.data[1])[2:].zfill(64)
        transaction_length = math.ceil(len("".join((self. header, self.base_serialize,
            partner_id, transaction_amount))) / 8 + 1)
        transaction_length = bin(transaction_length)[2:].zfill(8)
        result = "".join((self.header, transaction_length, self.base_serialize,
                         partner_id, transaction_amount))
        return self.decode(result)

    @staticmethod
    def deserialize(data):
        # data = int(data, 16)
        # data = bin(data)[2:]
        # data = "".join(("0", data))
        packet_length = int(binascii.hexlify(data)[4:6], 16)
        data = struct.unpack('B' * packet_length, data)
        data = list(map(lambda x: bin(x)[2:], data))
        header = int("".join((data[0].zfill(8), data[1].zfill(8))), 2)
        if header != 0x7a7a:
            return None
        t_time = list(map(lambda x: bin(int(x, 2))[2:].zfill(8), data[3:8]))
        t_time = "".join(t_time)
        t_type = int(data[20], 2)
        transaction_id = list(map(lambda x: bin(int(x, 2))[2:].zfill(8), data[8:16]))
        transaction_id = int("".join(transaction_id), 2)
        terminal_id = list(map(lambda x: bin(int(x, 2))[2:].zfill(8), data[16:20]))
        terminal_id = int("".join(terminal_id), 2)
        if t_type < 64:
            transaction_data = int(data[20], 2)
            return ServiceTransaction(terminal_id, transaction_id, ServiceTransaction.SERVICE_TYPES[transaction_data],
                                      t_time=t_time)
        elif 64 <= t_type < 128:
            raw_data = data[20][1:]
            raw_data += "".join(list(map(lambda x: bin(int(x, 2))[2:].zfill(8), data[21:32])))
            raw_data += bin(int(data[32], 2))[2:].zfill(2)
            t_amount = int(raw_data[32:], 2)
            t_id = int(raw_data[:32], 2)
            return PaymentTransaction(terminal_id, transaction_id, (t_id, t_amount), t_time=t_time)
        elif t_type >= 128:
            raw_data = data[20][2:]
            raw_data += "".join(list(map(lambda x: bin(int(x, 2))[2:].zfill(8), data[21:32])))
            raw_data += bin(int(data[32], 2))[2:].zfill(2)
            t_encashment = int(raw_data[32:], 2)
            t_collector_id = int(raw_data[:32], 2)
            return EncashmentTransaction(terminal_id, transaction_id, (t_collector_id, t_encashment), t_time=t_time)
        else:
            return None

    @staticmethod
    def decode(result):
        #result = int(result, 2)
        #result = bytes(hex(result), 'utf-8')
        to_pack = tuple()
        num_bytes = math.ceil(len(result) / 8)
        for i in range(0, num_bytes):
            slice = result[i * 8: (i + 1) * 8]
            slice = int(slice, 2)
            to_pack += (slice, )
        result = struct.pack('B' * num_bytes, *to_pack)
        return result


class ServiceTransaction(Transaction):

    SERVICE_TYPES = ['turn_on', 'shutdown', 'reload',
                        'act_sensor', 'blocking']

    def __init__(self, terminal_id, transaction_id, data, t_type='service', t_time=None):
        super().__init__(terminal_id, transaction_id, t_type, data, t_time)
        self.validate_data()

    def validate_data(self):
        if self.data not in self.SERVICE_TYPES:
            raise TransactionDataException(self)

    def serialize(self):
        transaction_data = bin(self.SERVICE_TYPES.index(self.data))[2:].zfill(3)
        transaction_length = math.ceil(len("".join((self.header, self.base_serialize,
                                              transaction_data))) / 8 + 1)

        transaction_length = bin(transaction_length)[2:].zfill(8)

        result = "".join((self.header, transaction_length, self.base_serialize,
                            transaction_data))
        return self.decode(result)

    def __str__(self):
        return "{} transaction: {}, with transaction_id = {}," \
               "terminal_id = {}".format(self.t_type, self.data,
                                         self.transaction_id,
                                         self.terminal_id)


class PaymentTransaction(Transaction):

    def __init__(self,terminal_id, transaction_id, data, t_type='payment', t_time=None):
        super().__init__(terminal_id, transaction_id, t_type, data, t_time)
        try:
            self.organization_id = self.data[0]
            self.t_amount = self.data[1]
        except (ValueError, IndexError):
            raise TransactionDataException(self)
        self.validate_data()

    def validate_data(self):
        if len(self.data) != 2:
            raise TransactionDataException(self)
        if not str(self.organization_id).isdigit() or not str(self.t_amount).isdigit():
            raise TransactionDataException(self)
        if self.organization_id <= 0 or self.organization_id > self.MAX_ID:
            raise TransactionDataException(self)
        if self.t_amount <= 0 or self.t_amount > self.MAX_AMOUNT:
            raise TransactionDataException(self)

    def __str__(self):
        result = "{} transaction with parameters: organization_id = {}," \
                 "amount = {}, terminal_id = {}, transaction_id = {}"\
            .format(self.t_type, self.organization_id, self.t_amount,
                    self.terminal_id, self.transaction_id)
        return result


class EncashmentTransaction(Transaction):

    def __init__(self,terminal_id, transaction_id, data, t_type="encashment", t_time=None):
        super().__init__(terminal_id, transaction_id, t_type, data, t_time)
        try:
            self.collector_id = self.data[0]
            self.encash_amount = self.data[1]
        except (ValueError, IndexError):
            raise TransactionDataException(self)
        self.validate_data()

    def validate_data(self):
        if len(self.data) != 2:
            raise TransactionDataException(self)
        if not str(self.collector_id).isdigit() or not str(self.encash_amount).isdigit():
            raise TransactionDataException(self)
        if self.collector_id <= 0 or self.collector_id > self.MAX_ID:
            raise TransactionDataException(self)
        if self.encash_amount <= 0 or self.encash_amount > self.MAX_AMOUNT:
            raise TransactionDataException(self)

    def __str__(self):
        result = "{} transaction with parameters: collector_id = {}, " \
                 "encashment = {}, terminal_id = {}, transaction_id = {}"\
            .format(self.t_type, self.collector_id, self.encash_amount,
                    self.terminal_id, self.transaction_id)
        return result


class TransactionTypeException(Exception):

    def __init__(self, transaction):
        super().__init__()
        self.transaction = transaction

    def __str__(self):
        return "Error in transaction type"


class TransactionDataException(Exception):

    def __init__(self, transaction):
        self.transaction = transaction

    def __str__(self):
        return "Error in {} transaction: invalid data {}".format(
            self.transaction.t_type, self.transaction.data)


def main():
    if __name__ == '__main__':
        pool = [ServiceTransaction(1, 324, 'reload'),
                PaymentTransaction(1, 2, [2, 7]),
                EncashmentTransaction(1, 3, [255, 99872]),
                PaymentTransaction(1, 4, (25, 9999222223333)),
                EncashmentTransaction(25, 5, [2, 123456]),
                PaymentTransaction(1, 6, (32, 12345))]
        for transaction in pool:
            serialized = transaction.serialize()
            #print(sys.getsizeof(serialized))
            deserialized = transaction.deserialize(serialized)
            print(deserialized)

main()
