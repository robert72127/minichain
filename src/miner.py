#how hard to mine should be dependent on nr of miners but we will use constant value
#hash of block has to be below some figure eg
# 00000000000000000a9550000000000000000000000000000000000000000000 in 2015

class Node:
    '''
    Node listen to transaction propagate it and try to mine a block

    it maintains blockchain (join network ask other nodes for history)

    assemble candidate for block
    node has to validate header and every transaction included in the block
    node will forward block only if it builds on the longest branch


    finds a nance that makes block valid (it's 32 bits)


   propagate, if all other miners accept you are rewarded


    '''
