#how hard to mine should be dependent on nr of miners but we will use constant value
#hash of block has to be start with some number of zeros
import rsa
import datetime

import Block

DIFF_TARGET = 8
NEW_BLOCK_AT = 4
TRANSACTIONS_IN_BLOCK = 20
WORK_PAYMENT = 6

class Node:
    '''
    Node listen for new transactions propagate them and try to mine a block

    assemble candidate for block
    node has to validate header and every transaction included in the block it received
    before propagating it

    once you assemble block propagate it
    and if all other miners accept you are rewarded

    state:
        mempoll
        list of neighbours
        list of unspend inputs
        blockchain
    '''
    def __init__(self, wallet, neighbours):
        self.wallet = wallet
        self.neighbours = neighbours
        self.mempoll = []
        self.blockchain = None
        self.unspend = {}
        i = 0
        while (self.blockchain, self.mempoll, self.unspend) != (None, None, None) and i < len(self.neighbours):
            (blockchain, mempoll, unspend) = self.neighbours[i].get_data()
            if blockchain != None and self.blockchain == None:
                self.blockchain = blockchain
            if mempoll != None and self.mempoll == None:
                self.mempoll = mempoll
            if unspend != None and self.unspend == None:
                self.unspend = unspend 

    def update_unspent(self):
        transactions = self.blockchain[:-1]
        for (sender, others, amounts, hash) in transactions:
            self.unspend[sender] = None

        for (sender, others, amounts, hash) in transactions:
            for  (address, amount) in zip(others, amounts):
                self.unspend[address].append({'hash':hash, 'amount':amount})
            

    def transactions_in(self, public_key):
        if public_key in self.unspend:
            return self.unspend[public_key]
        else:
            return None

    def get_balance(self, public_key):
        if public_key in self.unspend:
            return sum([amnt for amnt in self.transactions_in(public_key)]['amount'])
        else:
            return 0

    def get_data(self):
        return (dict(self.blockchain), self.mempoll, dict(self.unspend))

    def listen_transaction(self, public_key, other_public_keys, amounts, signature):
        #get transactions into walllet
        transactions_in = self.transactions_in(public_key)
        balance = self.get_balance(public_key)

        if balance >= sum(amounts):
            #sign message with amount you want to send
            message = ''
            message = [into[hash] for into in transactions_in].join('')
            message += amounts.join('')
            message += other_public_keys.join('')
            
            if rsa.verify(message, signature, public_key):

                transaction = [message, public_key, other_public_keys, amounts] 
                #receive, verify and add to mempoll
                if transaction not in self.mempoll:
                    self.mempoll.append(transaction)

                    #propagate to neighbours
                    for n in self.neighbours:
                        n.listen_transaction(self, public_key,other_public_keys, amounts, signature)


    def create_block(self):
        #check time
        if not datetime.datetime.now().minute % 4 == 0:
            return;

        transactions_cnt = 0
        amount_out = {}
        balances = {}
        transactions = []
        transactions.append([self.wallet.public_key, WORK_PAYMENT])

        #append transactions, set 1 aside for transaction appendig reward to miner
        i = 0
        while transactions_cnt < transactions_in_block - 1 and i < len(list(self.mempoll)):
            transaction  = self.mempoll[i]
            (public_key, others_public_key, amount, signature) = transaction
            if public_key not in balances:
                balances[public_key] = sum(self.get_balance(public_key))
            
            if balances[public_key] > amount_out:
                transactions.append(transaction)
                i += 1

            transactions_cnt += 1
            del self.mempoll.transactions[i]

        
        block = Block(self.blockchain[:-1].header.hash, transactions, DIFF_TARGET, self.blockchain[:-1])
        self.blockchain.append(block)
        
        self.update_unspent()
        
        for n in self.neighbours:
            if n.blockchain[:-1] != block:
                n.listen_block(block)

        
    def listen_block(self, block):
        #verify correctness
        if block.header.hash[0:self.diff_target] == [0 for i in target].join(''):
            
            block_ =  Block(block.prev_block_hash, block.transactions, DIFF_TARGET, block.nonce)
            if block_.header.hash == block.header.hash:
                self.blockchain.append(block)
                self.update_unspent 
            
                for n in self.neighbours:
                    if n.blockchain[:-1] != block:
                        n.listen_block(block)