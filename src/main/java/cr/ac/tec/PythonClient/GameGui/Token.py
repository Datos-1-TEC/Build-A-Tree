import sys
sys.path.append("..")
import json
from collections import namedtuple
from json import JSONEncoder
from Player import*
from types import SimpleNamespace

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
    return namedtuple('Token', tokenDict.keys())(*tokenDict.values())

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

def readChallenge():
    mainTokens = []
    fillerTokens = []
    file_path = 'JsonResources/CurrentChallenge.json'
    with open(file_path,'r') as read_file:
        data = json.load(read_file)

    data_dict = json.loads(data)
    #mainTokens_dict
    print(data_dict["Challenges"]["MainTokens"])
    print(data_dict["Challenges"]["FillerTokens"])
    mainTokens_dict = data_dict["Challenges"]["MainTokens"]
    fillerTokens_dict = data_dict["Challenges"]["FillerTokens"]

    for key in mainTokens_dict:
        token_dict = mainTokens_dict.get(key)
        token_string = json.dumps(token_dict)
        token_object = json.loads(token_string, object_hook=jsonToToken)
        print(token_object.value)
        myFinalToken = Token(token_object.value, token_object.shape)
        mainTokens.append(myFinalToken)
    print("Fin main tokens")

    for key in fillerTokens_dict:
        token_dict = fillerTokens_dict.get(key)
        token_string = json.dumps(token_dict)
        token_object = json.loads(token_string, object_hook=jsonToToken)
        myFinalToken = Token(token_object.value, token_object.shape)
        print(token_object.value)
        fillerTokens.append(myFinalToken)
    





#print(x.name, x.hometown.name, x.hometown.id)
readChallenge() 



