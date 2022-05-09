

class SocketConnector():

    def __init__(self, ip, port):
        #Initializing variables.

        self.ip = ip
        self.port = port

    def equals(self, connector):
        #Making sure that the node's connection details are or are not the same as the node calling it.
        #It's used to see if a connected node is or is not itself, in order to add other nodes to a list.
        
        if connector.ip == self.ip and connector.port == self.port:
            return True
        else:
            return False
