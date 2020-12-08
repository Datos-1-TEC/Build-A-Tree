import sys
sys.path.append("..")
import json
from collections import namedtuple
from json import JSONEncoder
from Player import*

class Token():
    def __init__(self, val, shape):
        super().__init__()
        self.val = val
        self.shape = shape
        self.points = 0

    
    def getVal(self):
        return self.val
    
    def getShape(self):
        return self.shape

    def getPoints(self):
        return self.points  

    def setPoints(self, points):
        self.points = points

def tokenToJson(token):
    string = json.dumps(token.__dict__)
    print("El token es: ")
    print(string)
    return string

def jsonToToken(tokenDict):
    return namedtuple('X', tokenDict.keys())(*tokenDict.values())

def parsedDict(dict , object_hook):
    token = json.loads(dict, object_hook=object_hook)
    return token
def sendToken(Token, playerID):
    jsonToken = json.dumps(Token.__dict__)
    data = {
        str(playerID):{
            "Token": {
                "shape": Token.getShape(),
                "value": Token.getVal()
            }
        }
    }
    with open('JsonResources/CurrentToken.json', 'w') as write_file:
        json.dump(data, write_file)
    message = json.dumps(data)
    print(message)
    return message



