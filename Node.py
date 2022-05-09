from Blockchain import Blockchain
from TransactionPool import TransactionPool
from Wallet import Wallet
from SocketCommunication import SocketCommunication
from NodeAPI import NodeAPI
from Message import Message
from BlockchainUtils import BlockchainUtils
import copy


class Node():

    def __init__(self, ip, port, key=None):
        #Initializing variables.

        self.p2p = None #An empty variable waiting to be declared as a Socket Communication class
        self.ip = ip #The IP of the node
        self.port = port #The communication port
        self.blockchain = Blockchain() #Assigning a blockchain class to the node.
        self.transactionPool = TransactionPool() #Assigning a transactionpool class to the node.
        self.wallet = Wallet() #Assigning a wallet to the node.
        if key is not None: #This allows us to read from a key pair, which should allow us to carry data from one node to another.
            self.wallet.readKeyPair(key)

    def startP2P(self): #This starts the socketcommunication class for this node
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication(self)

    def startAPI(self, apiPort): 
        #This will create and start an API for us to see the node's information in a browser.
        self.api = NodeAPI()
        self.api.injectNode(self)
        self.api.start(apiPort)

    def handleTransaction(self, transaction):
        #This handles all the processing of a transaction.

        #These lines gather the some of the nessesary data in the required format.
        data = transaction.payload()
        signature = transaction.signature
        signerPublicKey = transaction.senderPublicKey
        signatureValid = Wallet.signatureValid(data, signature, signerPublicKey)

        #This checks to see if a transaction is already in the transaction pool to prevent duplicated transactions.
        transactionExists = self.transactionPool.transactionExists(transaction)
        #This will check to see if the transaction is already in the blocks data before being sent.
        #If it meets the conditions below then it will be encoded, broadcasted across the blockchain and forged.
        transactionInBlock = self.blockchain.transactionExists(transaction)
        if not transactionExists and not transactionInBlock and signatureValid:
            self.transactionPool.addTransaction(transaction)
            message = Message(self.p2p.socketConnector,
                              'TRANSACTION', transaction)
            encodedMessage = BlockchainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)
            forgingRequired = self.transactionPool.forgingRequired()
            if forgingRequired:
                self.forge()

    def handleBlock(self, block):
        #This handles all the processing of a block.

        #Gathering nessesary data for the block.
        forger = block.forger
        blockHash = block.payload()
        signature = block.signature

        #A lot of validation checks to see if this block should be added to the chain (the names are self explanitory).
        blockCountValid = self.blockchain.blockCountValid(block)
        lastBlockHashValid = self.blockchain.lastBlockHashValid(block)
        forgerValid = self.blockchain.forgerValid(block)
        transactionsValid = self.blockchain.transactionsValid(
            block.transactions)
        signatureValid = Wallet.signatureValid(blockHash, signature, forger)

        #If the block count of the current block isn't valid then the entire chain is requested to update the count.
        if not blockCountValid:
            self.requestChain()
        #If all the checks pass the block is then added to the chain, transactions are removed from the pool and 
        #The new blockchain is then broadcasted to every node.
        if lastBlockHashValid and forgerValid and transactionsValid and signatureValid:
            self.blockchain.addBlock(block)
            self.transactionPool.removeFromPool(block.transactions)
            message = Message(self.p2p.socketConnector, 'BLOCK', block)
            self.p2p.broadcast(BlockchainUtils.encode(message))

    def handleBlockchainRequest(self, requestingNode):
        #Handles sending the blockchain from one node to another.
        message = Message(self.p2p.socketConnector,
                          'BLOCKCHAIN', self.blockchain)
        self.p2p.send(requestingNode, BlockchainUtils.encode(message))

    def handleBlockchain(self, blockchain):
        #This is the code responsible for handling BLOCKCHAIN messages when a node is out of sync with the current block count.
        localBlockchainCopy = copy.deepcopy(self.blockchain) #Creates a local copy of the nodes blockchain to compare against the recieved one.
        localBlockCount = len(localBlockchainCopy.blocks) #Checks the length of local block count
        receivedChainBlockCount = len(blockchain.blocks) #Checks the length of recieved block length
        if localBlockCount < receivedChainBlockCount: # Incrementally updates the blocks the node doesn't have
            for blockNumber, block in enumerate(blockchain.blocks):
                if blockNumber >= localBlockCount:
                    localBlockchainCopy.addBlock(block)
                    self.transactionPool.removeFromPool(block.transactions)
            self.blockchain = localBlockchainCopy

    def forge(self):
        #This code adds new blocks to the blockchain.
        #This checks if this node has a wallet which is the proposed forger of the next block.
        forger = self.blockchain.nextForger()
        if forger == self.wallet.publicKeyString(): #If there is the proposed forger it will create the next block and broadcast the block.
            print('i am the forger')
            block = self.blockchain.createBlock(
                self.transactionPool.transactions, self.wallet)
            self.transactionPool.removeFromPool(
                self.transactionPool.transactions)
            message = Message(self.p2p.socketConnector, 'BLOCK', block)
            self.p2p.broadcast(BlockchainUtils.encode(message))
        else: #If not it wont do anything.
            print('i am not the forger')

    def requestChain(self):
        #Handles sending a request for the chain to each node.
        message = Message(self.p2p.socketConnector, 'BLOCKCHAINREQUEST', None)
        self.p2p.broadcast(BlockchainUtils.encode(message))
