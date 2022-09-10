from hashlib import sha256

from merkle_tree import Merkle_Tree

class Header:
  '''
  Header contains block metadata
  nonce -  counter used for pow algoritm
  merkle_root - root of merkle tree consisting of all transactions in the block
  '''
  def __init__(self, prev_block_hash, merkle_root, nonce):
    self.prev_block_hash = prev_block_hash
    self.merkle_root = merkle_root
    self.nonce = nonce
    self.generate_hash()

  def generate_hash(self):
     self.hash = sha256(self.prev_block_hash + self.merkle_root + self.nonce)


class Block:
  '''
  Container data structure that aggregates transactions for inclusion in the public ledger
  args are self explanatory
  '''
  def __init__(self,prev_block_hash, transactions, diff_target, prev):
    self.previous = prev
    self.prev_block_hash = prev_block_hash
    self.transactions = transactions
    self.merkle_tree = Merkle_Tree.build(self.transactions)
    self.generate_block()

  def generate_block(self):
    nonce = 0
    header = Header(self.prev_block_hash, self.merkle_tree.data, nonce)
    while header.hash[0:self.diff_target] != [0 for i in target].join(''):
      nonce += 1
      header = Header(self.prev_block_hash, self.merkle_tree.data, nonce)
    self.nonce = nonce
    self.header = header