class Message():
    def __init__(self, senderConnector, messageType, data):
        #Initializing variables.

        self.senderConnector = senderConnector #This is the connected node the message is sending to.
        self.messageType = messageType #This is the type of message.
        self.data = data #This is the data of the message.
