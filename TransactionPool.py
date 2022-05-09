

class TransactionPool():

    def __init__(self):
        #This initializes an array for the transactions to be stored into.

        self.transactions = []

    def addTransaction(self, transaction):
        #This just appends each transaction to the array.

        self.transactions.append(transaction)

    def transactionExists(self, transaction):
        #Responsible for checking if a transaction being added is already in the transactions array.
        #If the transaction already exists it comes back as true, otherwise it is false.

        for poolTransaction in self.transactions:
            if poolTransaction.equals(transaction):
                return True
        return False

    def removeFromPool(self, transactions):
        #Responsible for creating a finalized transaction pool.
        #It loops through every transaction stored in transactions, if that transaction is already somehow in the transaction pool
        #it doesn't get inserted. Otherwise it gets put into the transaction pool which is then saved over the transactions array.

        newPoolTransactions = []
        for poolTransaction in self.transactions:
            insert = True
            for transaction in transactions:
                if poolTransaction.equals(transaction):
                    insert = False
            if insert == True:
                newPoolTransactions.append(poolTransaction)
        self.transactions = newPoolTransactions

    def forgingRequired(self):
        #This determines when a block is required to be forged based on the number of transactions that have taken place before the last block was forged.
        #It determines how fast a transaction will be processed. In this case it's just 1 (instantly).
        #This is bad for a real world situation because the amount of processing power needed would be huge, for this case it's fine.

        if len(self.transactions) >= 1:
            return True
        else:
            return False
