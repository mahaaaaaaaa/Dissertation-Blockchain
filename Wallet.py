from Crypto.PublicKey import RSA
from Transaction import Transaction
from Block import Block
from BlockchainUtils import BlockchainUtils
from Crypto.Signature import PKCS1_v1_5 #*1 This is a type of cryptography algorithm, I don't exactly understand the math
#behind it however there's documentation about it here:  https://datatracker.ietf.org/doc/html/rfc3447#section-7.2


class Wallet():

    def __init__(self):
        #This generates a RSA keypair (a public and private key) for a wallet to create transactions on the blockchain.
        #Using a keypair prevents fraudulent transactions from being created as a transaction cannot be signed
        #Without the keypair.

        self.keyPair = RSA.generate(2048)

    def readKeyPair(self, file):
        #This is used to read a keypair from a file. It's just used for the genisis node right now.
        #We need a genisis node in order to sign and create the first set of transactions on the blockchain.

        key = ''
        with open(file, 'r') as keyfile:
            key = RSA.importKey(keyfile.read())
        self.keyPair = key

    def sign(self, data):
        #Creating a signature for a transaction/block created by the wallet.

        dataHash = BlockchainUtils.hash(data) #Responsible for hashing the parsed data.
        signatureSchemeObject = PKCS1_v1_5.new(self.keyPair) #This generates a signature based off the keypair. *1
        signature = signatureSchemeObject.sign(dataHash) #We then sign the hashed data using that signature.
        return signature.hex() #Return it in a hexadecimal format.

    @staticmethod
    def signatureValid(data, signature, publicKeyString):
        #Responsible for validating the signature of the transaction/block.

        signature = bytes.fromhex(signature) #Creating a byte represention of the signature.
        dataHash = BlockchainUtils.hash(data) #Hashing the byte representation.
        publicKey = RSA.importKey(publicKeyString) #Importing the wallet's public key.
        signatureSchemeObject = PKCS1_v1_5.new(publicKey) #Creating a signature based off the public key of the wallet.
        signatureValid = signatureSchemeObject.verify(dataHash, signature) #Checks if the signature for the hash is valid

        return signatureValid

    def publicKeyString(self):
        #This is just used to output a string version of the public key of the wallet.

        publicKeyString = self.keyPair.publickey().exportKey(
            'PEM').decode('utf-8')
        return publicKeyString

    def createTransaction(self, receiver, amount, type):
        #Responsible for assigning the correct values for a transaction to take place.

        #A transaction consists of 4 different variables:
        #publicKeyString, the public keystring of the wallet sending the transaction.
        #receiver, the public keystring of the wallet receiving the transaction.
        #amount, the amount of some token being sent to the other user
        #type, the transaction type. This can be an exchange, transfer or stake transaction.

        transaction = Transaction(
            self.publicKeyString(), receiver, amount, type)
        signature = self.sign(transaction.payload()) #This is used to create a string signature for the transaction.
        transaction.sign(signature) #This signs the transaction, it can only use strings which is why we use a payload function above.
        return transaction

    def createBlock(self, transactions, lastHash, blockCount):
        #Responsible for assigning the correct values that make up a block in the blockchain.

        #A block consists of 4 different variables:
        #transactions, this is all of the transactions that take place in that block, currently it's set to 1 transaction per block.
        #lastHash, the hash value of the previous block. This is why we need a genisis block, otherwise there is no lasthash to put here.
        #publicKeyString, the public keystring of the wallet that created this block.
        #blockCount, the number of this block in the blockchain.

        block = Block(transactions, lastHash,
                      self.publicKeyString(), blockCount)
        signature = self.sign(block.payload()) #Just like in the transaction function. This is used to create a string signature for the block.
        block.sign(signature)#Also like in the transaction function. This signs the block.
        return block
