import rsa

import transaction

class Wallet:

    def __init__(self, closest_node):
        '''
        generate keys and set closest tconode
        '''
        self.closest_node = closest_node
        (self.public_key, self.private_key) = rsa.newkeys(512)


    def send(self, other_public_keys, amounts):
        '''
        send your adress, receipent adress and amount with proof to closest node 
        '''

        transactions_in = self.closest.node.transactions_in(self.id)

        balance = self.closest_node.get_balance(self.public_key)

        if balance > sum(amounts):
            #sign message with amount you want to send
            amount_to_self = balance  - sum(amounts)
            other_public_keys.append(self.public_key)
            amounts.append(amount_to_self)
            #concatenated hashes of into transactions, amount to send to each receipent, public keys
            message = ''
            message = [into[hash] for into in transactions_in].join('')
            message += amounts.join('')
            message += other_public_keys.join('')
            signature = rsa.sign(message.encode(), self.private_key, 'SHA-1')
        
        #broadcast
        self.closest_node.listen_transaction(self.public_key, other_public_keys, amounts, signature)
