import json
from collections import namedtuple
from json import JSONEncoder
class Token():
    def __init__(self, val, shape):
        super().__init__()
        self.val = val
        self.shape = shape
    
    def getVal(self):
        return self.val
    
    def getShape(self):
        return self.shape

def tokenToJson(token):
    string = json.dumps(token.__dict__)
    data = {
        "Token" : string
    }
    print(data)
    return string

def jsonToToken(tokenDict):
    return namedtuple('X', tokenDict.keys())(*tokenDict.values())

def parsedDict(dict , object_hook):
    token = json.loads(dict, object_hook=object_hook)
    return token

token = Token(12, "Triangle")


myToken = parsedDict(tokenToJson(token), jsonToToken)
print(myToken.val)
print(myToken.shape)

