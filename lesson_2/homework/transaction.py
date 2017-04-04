__author__ = "Kirill Cherkasov"

import sys
from datetime import datetime


class Transaction:
    '''
    реализация протокола
    '''

    MAX_AMOUNT = 18446744073709551614  # 8 байт
    MAX_ID = 4294967295   # 4 байта

    TRANSACTION_TYPES = ['service', 'payment', 'encashment']

    def __init__(self, t_type, data, t_time=None):
        self.header = '0111101001111010'  # 'zz'
        self.t_type = t_type
        self.data = data
        self.validate_type()
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
        transaction_type = bin(self.TRANSACTION_TYPES.index(self.t_type))[2:].zfill(2)
        return "".join((self.t_time, transaction_type))

    def serialize(self):
        transaction_id = bin(self.data[0])[2:].zfill(32)
        transaction_amount = bin(self.data[1])[2:].zfill(64)
        transaction_length = len("".join((self.base_serialize, transaction_id, transaction_amount)))
        transaction_length = bin(transaction_length)[2:].zfill(8)
        result = "".join((self.header, transaction_length, self.base_serialize,
                         transaction_id, transaction_amount))
        return bytes(result, 'utf-8')

    @staticmethod
    def deserialize(data):
        header = hex(int(data[:16], 2))
        if header != '0x7a7a':
            return None
        t_time = data[24:64]
        t_type = int(data[64:66], 2)
        if t_type == 0:
            transaction_data = int(data[66:69], 2)
            return ServiceTransaction(ServiceTransaction.SERVICE_TYPES[transaction_data],
                                      t_time=t_time)
        elif t_type == 1:
            t_amount = int(data[98:162], 2)
            t_id = int(data[66:98], 2)
            return PaymentTransaction((t_id, t_amount), t_time=t_time)
        elif t_type == 2:
            t_encashment = int(data[98:162], 2)
            t_collector_id = int(data[66:98], 2)
            return EncashmentTransaction((t_collector_id, t_encashment), t_time=t_time)
        else:
            return None


class ServiceTransaction(Transaction):

    SERVICE_TYPES = ['turn_on', 'shutdown', 'reload',
                        'act_sensor', 'blocking']

    def __init__(self, data, t_type='service', t_time=None):
        super().__init__(t_type, data, t_time)
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

    def __str__(self):
        return " ".join((self.t_type, "transaction:", self.data))


class PaymentTransaction(Transaction):

    def __init__(self, data, t_type='payment', t_time=None):
        super().__init__(t_type, data, t_time)
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
                 "amount = {}".format(self.t_type, self.organization_id,
                                      self.t_amount)
        return result


class EncashmentTransaction(Transaction):

    def __init__(self, data, t_type="encashment", t_time=None):
        super().__init__(t_type, data, t_time)
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
                 "encashment = {}".format(self.t_type, self.collector_id,
                                          self.encash_amount)
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
        t2 = ServiceTransaction('reload')
        t3 = PaymentTransaction([2, 7])
        t4 = EncashmentTransaction([1, 1])
        t2.serialize()
        s2 = t2.serialize()
        s3 = t3.serialize()
        s4 = t4.serialize()
        t5 = PaymentTransaction((25, 1000))
        s5 = t5.serialize()
        ds2 = t2.deserialize(s2)
        ds3 = t2.deserialize(s3)
        ds4 = t2.deserialize(s4)
        ds5 = t2.deserialize(s5)
        print(ds2)
        print(ds3)
        print(ds4)
        print(ds5)

main()
