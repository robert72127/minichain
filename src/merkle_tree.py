
from hashlib import sha256
import hashlib

class Merkle_Node:

    def __init__(self, left, right, data):
        self.left = left
        self.right = right
        self.data = self._hash(data)

    def __str__(self):
        return self.data

    def _hash(self, data):
        return sha256(data.encode('utf-8')).hexdigest()

    def copy():
        return Merkle_Node(self.left, self,right, self.type, self.data)
    
class Merkle_Tree:

    @staticmethod
    def build(values):
        nodes = [ Merkle_Node(None, None, v) for v in values]
        length = len(nodes)

        if (length % 2):
            nodes.append(nodes[-1].copy())
            length += 1
        
        if (length == 2):
            return Merkle_Node(nodes[0], nodes[1], nodes[0].data+nodes[1].data)
        
        else:
            left  = Merkle_Tree.build(values[:length//2])
            right = Merkle_Tree.build(values[length//2:])
            return Merkle_Node(left, right, left.data+right.data)