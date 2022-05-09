#RUN 'py -m pip install -r requirements.txt' TO INSTALL ALL THE LIBRARIES NESSESARY ON A DIFFERENT COMPUTER!!!!!!!!!!!!!!!!!

# Commands to run the whole blockchain locally.
#------------------------------------------------------------------
# python main.py localhost 10000 5000 keys/genesisPrivateKey.pem
# python main.py localhost 10001 5001 keys/stakerPrivateKey.pem
# python interaction.py

from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
from Node import Node
import sys

if __name__ == '__main__':
    ip = sys.argv[1] # System argument for the node's IP address, to run locally use localhost
    port = int(sys.argv[2]) # System argument for the node's communication port, use a rarely used port like 10000
    apiPort = int(sys.argv[3]) # System argument for the node's API communication port, use a rarely used port like 5000
    
    #This argument is only nessesary for the genesis node
    keyFile = None 
    if len(sys.argv) > 4:
        keyFile = sys.argv[4]

    node = Node(ip, port, keyFile)
    node.startP2P()
    node.startAPI(apiPort)

#CURRENT ISSUES

#Transaction Pool and blockchain struggle to list everything.
#All interactions appear in /blockchain for the nodes but not /transactionPool, not sure why??
#All forgers in the blockchain appear to have the same key, even when the nodes terminals disagree with this??
#Sometimes the account model mischecks the amount tied to a wallet's key, a larger amount than an account balance
#manages to get through.