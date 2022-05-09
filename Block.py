import time
import copy


class Block():

    def __init__(self, transactions, lastHash, forger, blockCount):
        #Initializing variables.

        self.blockCount = blockCount #Block count of the current block.
        self.transactions = transactions #The transactions taking place this block.
        self.lastHash = lastHash #The hash of the last block.
        self.timestamp = time.time() #The time the block was created.
        self.forger = forger #The 
        self.signature = ''

    @staticmethod
    def genesis():
        #This is a function to generate the "Genesis block".
        #Every blockchain needs a first block which to base the next hash off of, this just simply creates it.

        genesisBlock = Block([], 'genesisHash', 'genesis', 0)
        genesisBlock.timestamp = 0
        return genesisBlock

    def toJson(self):
        #This function converts the block's data into a JSON format. This mainly done because it prints out in a
        #readable format, but other libraries will also only work in a JSON format.
        data = {}
        data['blockCount'] = self.blockCount
        data['lastHash'] = self.lastHash
        data['signature'] = self.signature
        data['forger'] = self.forger
        data['timestamp'] = self.timestamp
        jsonTransactions = []
        for transaction in self.transactions:
            jsonTransactions.append(transaction.toJson())
        data['transactions'] = jsonTransactions
        return data

    def payload(self):
        #Creating a string out of the data parsed to the function.

        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation['signature'] = ''
        return jsonRepresentation

    def sign(self, signature):
        #Signs the block with a
        self.signature = signature
