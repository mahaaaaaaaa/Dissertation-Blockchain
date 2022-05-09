from Crypto.Hash import SHA256
import json
import jsonpickle


class BlockchainUtils():

    #Using static methods just so I can call the functions without having to create extra instances of the 
    #BlockchainUtils class, since it's used in a lot of places it's just easier this way.
    @staticmethod
    def hash(data):
        #The purpose of the function is to convert data to a generalized data format.
        #Data can be almost anything, that's why I dump it as a JSON so basically anything can be worked with.
        dataString = json.dumps(data) #Converts data into a string.
        dataBytes = dataString.encode('utf-8') #Converts that string into a byte format.
        dataHash = SHA256.new(dataBytes) #Hashes the byte string.
        return dataHash

    @staticmethod
    def encode(objectToEncode):
        #This will encode some data, used before sending messages across the blockchain.

        return jsonpickle.encode(objectToEncode, unpicklable=True)

    @staticmethod
    def decode(encodedObject):
        #This will decode data once it reaches another node.
        return jsonpickle.decode(encodedObject)
