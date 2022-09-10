#how hard to mine should be dependent on nr of miners but we will use constant value
#hash of block has to be start with some number of zeros
import rsa
import datetime

import Block

diff_target = 8
new_block_at = 4
transactions_in_block = 20

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

    def get_balance(self, public_key):
        return self.mempoll[public_key]

    def get_data(self):
        return (dict(self.blockchain), self.mempoll, dict(self.unspend))

    def listen_transaction(self, public_key, others_public_key, amount_out, amount_self, signature):
        #get transactions into walllet
        transactions_in = self.get_balance(public_key)
        balance = [into['amount'] for into in transactions_in]

        if balance >= sum(amount_out):
            #sign message with amount you want to send
            amount_to_self = balance  - sum(amount_out)
            claimable = balance - amount_to_self - amount_out
            message = ''
            message = [into[hash] for into in transactions_in].join('')
            message += amount_out + amount_to_self
            message += others_public_key + self.public_key
            
            if rsa.verift(message, signature, public_key):

                transaction = [message, public_key, transactions_in, others_public_key, amount_out, amount_self, claimable] 
                #receive, verify and add to mempoll
                if transaction not in self.mempoll:
                    self.mempoll.append(transaction)

                    #propagate to neighbours
                    for n in self.neighbours:
                        n.listen_transaction(self, public_key, others_public_key, amount_out, amount_self, signature)

        
        
    def listen_block(self, block):
        #verify correctness

        #check validity of each transaction

        #recreate tree with nonce

        #if both correct append to blockchain and update balances

        pass

    def create_block(self):
        #check time
        if not datetime.datetime.now().minute % 4 == 0:
            return;

        transactions_cnt = 0
        amount_out = {}
        balances = {}
        transactions = []
        transactions.append([self.wallet.public_key, to_claim])
        to_claim = 0
        #append transactions, set 1 aside for transaction appendig reward to miner
        i = 0
        while transactions_cnt < transactions_in_block - 1 and i < len(list(self.mempoll)):
            transaction  = self.mempoll[i]
            (message, public_key, transactions_in, others_public_key, amount_out, claimable) = transaction
            if public_key not in balances:
                balances[public_key] = sum(self.get_balance(public_key))
            
            if balances[public_key] > amount_out:
                transactions.append(transaction)
                to_claim += claimable
                i += 1
            transactions_cnt += 1
            del self.mempoll.transactions[i]
        transactions[0][1] = to_claim
        
        block = Block(self.blockchain[:-1].header.hash, transactions, diff_target, self.blockchain[:-1])
        self.blockchain.append(block)
        
        #update unspent        
        

        for n in self.neighbours:
            n.listen_block(block)
