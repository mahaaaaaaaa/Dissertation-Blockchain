from Wallet import Wallet
from BlockchainUtils import BlockchainUtils
import requests


def postTransaction(sender, receiver, amount, type):
    #This will post the type of transaction to the master node.

    #Creating a transaction consisting of the recieving adresses publickey, the amount and type of transaction
    transaction = sender.createTransaction(receiver.publicKeyString(), amount, type)
    url = "http://localhost:5000/transaction" #URL of the master node
    package = {'transaction': BlockchainUtils.encode(transaction)} #Encoding the transaction into the proper format.
    request = requests.post(url, json=package) #Posting the transaction to the URL as a JSON.


#THIS IS WHAT WILL BE POSTED TO THE BLOCKCHAIN.
#AN EXCHANGE TRANSACTION JUST CREATES THE TOKEN OUT OF NOWHERE FOR DEMONSTRATION PURPOSES.
if __name__ == '__main__':

    wallet1 = Wallet()
    wallet2 = Wallet()
    wallet2.readKeyPair('keys/stakerPrivateKey.pem') #Just an example of reading from a pre-generated key,
    #Reading from a pre-generated key can tie a wallet to a node.
    exchange = Wallet()

     
    postTransaction(exchange, wallet2, 100, 'EXCHANGE')
    postTransaction(exchange, wallet1, 100, 'EXCHANGE')
    postTransaction(exchange, wallet1, 10, 'EXCHANGE')


    postTransaction(wallet2, wallet2, 25, 'STAKE')
    postTransaction(wallet2, wallet1, 1, 'TRANSFER')
    postTransaction(wallet2, wallet1, 1, 'TRANSFER')

    postTransaction(wallet2, wallet1, 80, 'TRANSFER')
