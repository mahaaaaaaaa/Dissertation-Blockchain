#This class is be responsible for storing the balance of known accounts.

class AccountModel():

    def __init__(self):
        self.accounts = []
        self.balances = {}

    def addAccount(self, publicKeyString):
        #This function adds user's public keys to the account list if they are not already on there.

        if not publicKeyString in self.accounts:
            self.accounts.append(publicKeyString)
            self.balances[publicKeyString] = 0

    def getBalance(self, publicKeyString):
        #This function will return the balance assosiated with the parsed public key.

        if publicKeyString not in self.accounts:
            self.addAccount(publicKeyString)
        return self.balances[publicKeyString]

    def updateBalance(self, publicKeyString, amount):
        #Responsible for updating the balance of the account assosiated with the parsed public key.
        
        if publicKeyString not in self.accounts:
            self.addAccount(publicKeyString)
        self.balances[publicKeyString] += amount
