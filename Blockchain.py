from Block import Block
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
from ProofOfStake import ProofOfStake


class Blockchain():

    def __init__(self):
        #Initializing variables.

        self.blocks = [Block.genesis()] #Setting the first block to the genesis block.
        self.accountModel = AccountModel() #Defining a class responsible for the account model (logic for account balance)
        self.pos = ProofOfStake() #Defining a class responsible for the proof of stake logic.

    def addBlock(self, block):
        #Adding blocks to the blockchain.

        self.executeTransactions(block.transactions) #Execute the transactions for this block.
        self.blocks.append(block) #Append the block's information to the blockchain.

    def toJson(self):
        #Converts the blockchain's data to JSON for readability.

        data = {}
        jsonBlocks = []
        for block in self.blocks:
            jsonBlocks.append(block.toJson())
        data['blocks'] = jsonBlocks
        return data

    def blockCountValid(self, block):
        #Making sure that the block being added is the correct count.

        if self.blocks[-1].blockCount == block.blockCount - 1:
            return True
        else:
            return False

    def lastBlockHashValid(self, block):
        #Making sure that the hash of the current block is valid to the hash of the previous block.
        #This insures blockchain integrity.

        latestBlockchainBlockHash = BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest()
        if latestBlockchainBlockHash == block.lastHash:
            return True
        else:
            return False

    def getCoveredTransactionSet(self, transactions):
        #This creates a set of transactions that are covered by the accounts total balance.

        coveredTransactions = [] #Creating an array for covered transactions to go into.
        for transaction in transactions:
            if self.transactionCovered(transaction):
                coveredTransactions.append(transaction) #If the transaction is covered it gets added.
            else:
                print('transaction is not covered by sender') #Otherwise this line gets printed and is not appended to coveredTransaction.
        return coveredTransactions

    def transactionCovered(self, transaction):
        #This has the logic to check if a transaction is covered or not.

        if transaction.type == 'EXCHANGE': #This is a way for an account to get some 'token' without owning any.
            return True
        senderBalance = self.accountModel.getBalance(transaction.senderPublicKey) #Gets the balance tied to a public key.
        if senderBalance >= transaction.amount: #If their balance is = or over the transaction amount it's ok. Otherwise it shouldn't send.
            return True
        else:
            return False

    def executeTransactions(self, transactions):
        #Responsible for executing all the transactions for the block by running the code in the function below.

        for transaction in transactions:
            self.executeTransaction(transaction)

    def executeTransaction(self, transaction):
        #Logic behind executing different transaction types.

        #Staking gives a public key tied to a node a chance to be the forger of the new block.
        #This will remove balance from an account and update the proof of stake logic to give the node with
        #the public key a chance in relation to how much is staked to forge the new block.
        #e.g if two nodes have 1 token staked each, they both have a 50/50 chance tobe chosen to forge the new block.

        if transaction.type == 'STAKE':
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            if sender == receiver:
                amount = transaction.amount
                self.pos.update(sender, amount)
                self.accountModel.updateBalance(sender, -amount)
        else: #Else assumes that this is a transfer, since it's the only other type of transaction left.
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            amount = transaction.amount
            self.accountModel.updateBalance(sender, -amount)
            self.accountModel.updateBalance(receiver, amount)

    def nextForger(self):
        lastBlockHash = BlockchainUtils.hash(
            self.blocks[-1].payload()).hexdigest()
        nextForger = self.pos.forger(lastBlockHash)
        return nextForger

    def createBlock(self, transactionsFromPool, forgerWallet):
        #Responsible for creating a new block.

        #This gets the list of covered transactions and executes them.
        coveredTransactions = self.getCoveredTransactionSet(transactionsFromPool)
        self.executeTransactions(coveredTransactions)

        #This will convert the new block's data into a string
        newBlock = forgerWallet.createBlock(coveredTransactions, BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest(), len(self.blocks))
        self.blocks.append(newBlock) #This will append it to the blockchain.
        return newBlock

    def transactionExists(self, transaction):
        #Responsible for checking if a transaction is already in the block.

        for block in self.blocks:
            for blockTransaction in block.transactions:
                if transaction.equals(blockTransaction):
                    return True
        return False

    def forgerValid(self, block):
        #Checks to see if the forger is valid to forger the next block by seeing if the proposed block forger
        #is the forger that was nominated to forge it.

        forgerPublicKey = self.pos.forger(block.lastHash)
        proposedBlockForger = block.forger
        if forgerPublicKey == proposedBlockForger:
            return True
        else:
            return False

    def transactionsValid(self, transactions):
        #Checks to see if the transactions being appended to the block are valid by comparing the length of
        #both the covered and appended transactions are the same.
        
        coveredTransactions = self.getCoveredTransactionSet(transactions)
        if len(coveredTransactions) == len(transactions):
            return True
        return False
