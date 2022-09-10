import rsa

import transaction

class Wallet:

    def __init__(self, closest_node):
        '''
        generate keys and set closest tconode
        '''
        self.closest_node = closest_node
        (self.public_key, self.private_key) = rsa.newkeys(512)

    #downolad headers
    def get_balance(self):
       return self.closest_node.get_balance(self.public_key) 

    def send(self, other_public_key, amount_in, amount_out):
        '''
        send your adress, receipent adress and amount with proof to closest node 
        '''

        transactions_in = self.closest.node.transactions_in(self.id)
        balance = [into['amount'] for into in transactions_in]

        if balance > amount_in and amount_out <= amount_in:
            #sign message with amount you want to send
            amount_to_self = balance  - amount_out

            #concatenated hashes of into transactions, amount to send to each receipent, public keys
            message = ''
            message = [into[hash] for into in transactions_in].join('')
            message += amount_out + amount_to_self
            message += other_public_key + self.public_key
            
            signature = rsa.sign(message.encode(), self.private_key, 'SHA-1')
        
        #broadcast
        self.closest_node.listen_transaction(self.public_key, other_public_key, amount_out, signature)
