from BlockchainUtils import BlockchainUtils


class Lot():
    def __init__(self, publicKey, staked, lastBlockHash):
        #Initializing variables

        self.publicKey = str(publicKey) #Public key of the account creating lots
        self.staked = staked #Correlates with the amount staked, this is how many times 
        self.lastBlockHash = str(lastBlockHash)

    def lotHash(self):
        #Hashes the lot data before sending across the blockchain.
        hashData = self.publicKey + self.lastBlockHash
        for _ in range(self.staked):
            hashData = BlockchainUtils.hash(hashData).hexdigest()
        return hashData
