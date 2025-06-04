import random
import hashlib

# -----------------------
# Constants
# -----------------------
literalCharSet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#%()*+,-./:;=?@[]^_`{|}~"
charsetLength = len(literalCharSet)

# -----------------------
# pypenguin_old.utility Classes
# -----------------------
class LocalStringToToken:
    def __init__(self, main: str, spriteName=None):
        self.main = main
        self.spriteName = spriteName

    def __repr__(self):
        return f"LocalStringToToken(main={repr(self.main)}, spriteName={repr(self.spriteName)})"

    def toToken(self):
        return stringToToken(main=self.main, spriteName=self.spriteName)

    def toJSON(self):
        return {"_custom_": True, "_type_": "LocalStringToToken", "main": self.main}

# -----------------------
# String Tokenization Functions
# -----------------------
def stringToToken(main: str, spriteName=None) -> str:
    def convert(inputString: str, digits: int) -> str:
        hashObject = hashlib.sha256(inputString.encode())
        hexHash = hashObject.hexdigest()

        result = []
        for i in range(digits):
            chunk = hexHash[i * 2:(i * 2) + 2]
            index = int(chunk, 16) % charsetLength
            result.append(literalCharSet[index])

        return ''.join(result)

    if spriteName is None:
        return convert(main, digits=20)
    else:
        return convert(spriteName, digits=4) + convert(main, digits=16)

def generateRandomToken():
    return ''.join(random.choice(literalCharSet) for _ in range(20))

def literalToNumber(literal):
    base = len(literalCharSet)
    num = 0
    for i, char in enumerate(reversed(literal)):
        num += (literalCharSet.index(char) + 1) * (base ** i)
    return num

def numberToLiteral(number):
    base = len(literalCharSet)
    result = []
    while number > 0:
        number -= 1
        result.append(literalCharSet[number % base])
        number //= base
    return ''.join(reversed(result))

def generateNextKeyInDict(obj: dict, offset=0):
    keys = list(obj.keys())
    ints = [literalToNumber(i) for i in keys]
    biggest = max([0] + ints)
    return numberToLiteral(biggest + 1 + offset)
