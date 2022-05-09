from p2pnetwork.node import Node
from PeerDiscoveryHandler import PeerDiscoveryHandler
from SocketConnector import SocketConnector
from BlockchainUtils import BlockchainUtils
import json


class SocketCommunication(Node):

    def __init__(self, ip, port):
        #Initializing variables.

        super(SocketCommunication, self).__init__(ip, port, None)
        self.peers = [] #A list of a nodes connected nodes called peers.
        self.peerDiscoveryHandler = PeerDiscoveryHandler(self) #Defining a class responsible for finding other connected nodes.
        self.socketConnector = SocketConnector(ip, port) #Defining a class for handling the connection details.

    def connectToFirstNode(self):
        #A hard coded route for a node to connect with other nodes through a 'master' node of sorts.
        #This was the only way I really know how to connect them together, if I wanted to connect over a network this would 
        #need to be the master node's ip address on port 10000 (I'm guessing since I can't test right now).

        if self.socketConnector.port != 10000:
            self.connect_with_node('localhost', 10000)

    def startSocketCommunication(self, node):
        #Responsible for starting communication with other nodes.

        self.node = node #Defines an instance of a P2P node.
        self.start() #Starts a thread of the node instance.
        self.peerDiscoveryHandler.start() #Starts a thread of the peer discovery
        self.connectToFirstNode() #Connects to the master node. This node will echo all other connected nodes to each node.

    def inbound_node_connected(self, connected_node):
        #Handshakes with the connected node for communication.
        self.peerDiscoveryHandler.handshake(connected_node)

    def outbound_node_connected(self, connected_node):
        #Handshakes with the connected node for communication.
        self.peerDiscoveryHandler.handshake(connected_node)

    def node_message(self, connected_node, message):
        #Responsible for handling a formatted message from other nodes depending on the type of message it is.
        #The type of a message and all information is pre-defined in each class.

        message = BlockchainUtils.decode(json.dumps(message))
        if message.messageType == 'DISCOVERY':
            self.peerDiscoveryHandler.handleMessage(message)
        elif message.messageType == 'TRANSACTION':
            transaction = message.data
            self.node.handleTransaction(transaction)
        elif message.messageType == 'BLOCK':
            block = message.data
            self.node.handleBlock(block)
        elif message.messageType == 'BLOCKCHAINREQUEST':
            self.node.handleBlockchainRequest(connected_node)
        elif message.messageType == 'BLOCKCHAIN':
            blockchain = message.data
            self.node.handleBlockchain(blockchain)

    def send(self, receiver, message):
        #Sends a message to a SINGLE node.

        self.send_to_node(receiver, message)

    def broadcast(self, message):
        #Broadcasts a message to EVERY connected node.
        self.send_to_nodes(message)
