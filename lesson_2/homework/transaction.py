__author__ = "Kirill Cherkasov"

import sys
from datetime import datetime


class Transaction:

    MAX_AMOUNT = 18446744073709551614  # 8 байт
    MAX_ID = 4294967295   # 4 байта

    TRANSACTION_TYPES = ['service', 'payment', 'encashment']

    def __init__(self, t_type, data):
        self.header = '0111101001111010'  # 'zz'
        self.t_type = t_type
        self.data = data
        self.validate_type()

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

    @staticmethod
    def decode_time(binary_time):
        year = binary_time[:7]
        year = int(year, 2) + 2000
        month = int(binary_time[7:11], 2)
        day = int(binary_time[11:16], 2)
        seconds = int(binary_time[16:], 2)
        hours = seconds // 3600
        minutes = (seconds - hours * 3600) // 60
        seconds = seconds - hours * 3600 - minutes * 60
        result = "{:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(year, month, day,
                                                                    hours, minutes, seconds)
        return result

    @property
    def base_serialize(self):
        transaction_time = self.get_time()
        transaction_type = bin(self.TRANSACTION_TYPES.index(self.t_type))[2:].zfill(2)
        return "".join((transaction_time, transaction_type))

    def serialize(self):
        transaction_id = bin(self.data[0])[2:].zfill(32)
        transaction_amount = bin(self.data[1])[2:].zfill(64)
        transaction_length = len("".join((self.base_serialize, transaction_id, transaction_amount)))
        transaction_length = bin(transaction_length)[2:].zfill(8)
        result = "".join((self.header, transaction_length, self.base_serialize,
                         transaction_id, transaction_amount))
        return bytes(result, 'utf-8')


class ServiceTransaction(Transaction):

    SERVICE_TYPES = ['turn_on', 'shutdown', 'reload',
                        'act_sensor', 'blocking']

    def __init__(self, data, t_type='service'):
        super().__init__(t_type, data)
        self.validate_data()

    def validate_data(self):
        if self.data not in self.SERVICE_TYPES:
            raise TransactionDataException(self)

    def serialize(self):
        transaction_data = bin(self.SERVICE_TYPES.index(self.data))[2:].zfill(3)
        transaction_length = bin(len("".join((self.base_serialize,
                                              transaction_data))))[2:].zfill(8)

        result = "".join((self.header, transaction_length, self.base_serialize,
                            transaction_data))

        return bytes(result, 'utf-8')


class PaymentTransaction(Transaction):

    def __init__(self, data, t_type='payment'):
        super().__init__(t_type, data)
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
        print(self.t_amount)
        if self.t_amount <= 0 or self.t_amount > self.MAX_AMOUNT:
            raise TransactionDataException(self)


class EncashmentTransaction(Transaction):

    def __init__(self, data, t_type="encashment"):
        super().__init__(t_type, data)
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
        t2 = ServiceTransaction('reload')
        t3 = PaymentTransaction([2, 7])
        t4 = EncashmentTransaction([1, 1])
        t2.serialize()
        print(t2.serialize())
        print(t3.serialize())
        print(t4.serialize())
        t5 = PaymentTransaction((25, 1000))
        print(t5.serialize())
main()
