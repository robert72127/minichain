import random

class Mempoll:
    
    def __init__(self):
        self.transactions = {}

    def add(self, id_sender, id_receiver, amount, transaction_id):
        self.transactions[transaction_id] = dict(sender = id_sender, receiver = id_receiver, amount = amount)

class State:
    def __init__(self):
        self.balances = {}

    def get_balance(self, id):
        if id not in self.balances:
            return 0
        else:
            return self.balances[id]

class Wallet:

    def __init__(self, id, closest):
        '''
        keys and into transactions hash, showing balance?
        '''
        self.id = id
        self.closest_node = closest

    def get_balance(self):
        if self.closest_node:
            return self.closest_node.state.get_balance(self.id)
        else:
            return 0

    def send(self, other, amount):
        '''
        Point to last transaction where you received coins
        send amount to other and balance - amount to self 

        To ensure money wasn't spend scan all transactions in between
        '''
        if self.get_balance() >= amount:
            self.closest_node.mempoll.add(self.id, other.id, amount,random.randint(0, 100000))

class Miner:

    def __init__(self,tax,wallet):
        self.state = State()
        self.mempoll = Mempoll()
        self.tax = tax
        self.wallet = wallet

    def mine(self):
        balances = dict(self.state.balances)
        print(balances)
        count = 0
        for key in list(self.mempoll.transactions.keys()):
            (sender, receiver, amount) = self.mempoll.transactions[key].values()
            if balances[sender] >= amount:
                balances[sender] -= amount 
                balances[receiver] += amount * (1-self.tax)
                balances[self.wallet.id] += amount * self.tax
                count += 1
            del self.mempoll.transactions[key]
        self.state.balances = dict(balances)


if __name__ == '__main__':
    user_miner = Wallet(0, None)
    miner = Miner(0.5, user_miner)
    user_miner.closest_node = miner
    user_1 = Wallet(1,miner)
    user_2 = Wallet(2, miner)


    miner.state.balances[1] = 100.
    miner.state.balances[2] = 100.
    miner.state.balances[0] = 0.

    print(miner.state.get_balance(0))
    print(miner.state.get_balance(1))
    print(miner.state.get_balance(2))
    print()
    print()
    print()


    user_1.send(user_2, 20.)
    print(miner.mempoll.transactions)
    print(miner.state.balances)
    miner.mine()

    print(miner.state.get_balance(0))
    print(miner.state.get_balance(1))
    print(miner.state.get_balance(2))
