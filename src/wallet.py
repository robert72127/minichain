class Wallet:

    def __init__(self):
        '''
        keys and into transactions hash, showing balance?
        '''
        pass

    def send(self, other_public_key, amount):
        '''
        Point to last transaction where you received coins
        send amount to other and balance - amount to self 

        To ensure money wasn't spend scan all transactions in between
        '''
        pass

    def receive(self, amount):
        '''
        create transaction with two inputs last recent, and previous stored
        '''
        pass


class Transaction
