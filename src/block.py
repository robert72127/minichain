from hashlib import sha256

class Header:
  '''
  Header consist of sets of block metadata 
  nonce -  counter used for pow algoritm
  other args are self explanatory
  '''
  def __init__(self, version, prev_block_hash, merkle_root, timestamp, diff_target, nonce):
    self.version = version
    self.prev_block_hash = prev_block_hash
    self.merkle_root = merkle_root
    self.timestamp = timestamp
    self. diff_target = diff_target
    self.nonce = nonce


class Block:
  '''
  Container data structure that aggregates transactions for inclusion in the public ledger
  args are self explanatory


  Block is group of transactions

  Each block
  has a block header, a hash pointer to some transaction data, and a
  hash pointer to the previous block in the sequence

  '''
  def __init__(self, block_size, block_header, transaction_counter, transactions,):
    self.block_size = block_size
    self.block_header = block_header
    self.block_counter = transaction_counter
    self.block_transactions = transactions

  def encode(self):
    '''
    return hash sha256 of current block
    '''
    return(sha256("test".encode('utf-8')).hexdigest())
  