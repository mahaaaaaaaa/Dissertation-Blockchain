import uuid
import time
import copy


class Transaction():

    def __init__(self, senderPublicKey, receiverPublicKey, amount, type):
        #Initializing variables.

        self.senderPublicKey = senderPublicKey #Public key of the user sending.
        self.receiverPublicKey = receiverPublicKey #Public key of the user recieving.
        self.amount = amount #The amount being sent.
        self.type = type #The type of transaction.
        self.id = (uuid.uuid1()).hex #Creating a unique id of the transaction. Making it hexadecimal to make it shorter.
        self.timestamp = time.time() #The time of the transaction being initialised.
        self.signature = '' #Creating an empty string for the signature hash to be stored into.

    def toJson(self):
        #Creating a JSON dictionary consisting of every variable in the initializer.

        return self.__dict__ 

    def sign(self, signature):
        #Just assigning the signature to the parsed signature.

        self.signature = signature 

    def payload(self):
        #Creating a string out of the data parsed to the function.

        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation['signature'] = ''
        return jsonRepresentation

    def equals(self, transaction):
        #Used to see if a transaction in a blocks list of transactions or the transaction pool.

        if self.id == transaction.id:
            return True
        else:
            return False
