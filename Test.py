from ProofOfStake import ProofOfStake
from Lot import Lot
import string
import random


def getRandomString(length):
    letters = string.ascii_lowercase
    resultString = ''.join(random.choice(letters) for i in range(length))
    return resultString


if __name__ == '__main__':
    pos = ProofOfStake()
    pos.update('bloke', 100)
    pos.update('human', 100)

    blokeWIN = 0
    humanWIN = 0

    for i in range(100):
        forger = pos.forger(getRandomString(i))
        if forger == 'bloke':
            blokeWIN += 1
        elif forger == 'human':
            humanWIN += 1

    print('bloke won: ' + str(blokeWIN) + ' times')
    print('human won: ' + str(humanWIN) + ' times')
