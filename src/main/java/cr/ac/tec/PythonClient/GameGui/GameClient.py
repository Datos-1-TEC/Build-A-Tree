import sys
import socket as sk
import json
from threading import*
from json import JSONEncoder
from Player import*
from Token import*
from collections import namedtuple
host = "127.0.0.1"
port = 6666
flag = True
format = "utf8"
bts = 4096

firstMessage = "Connected"
class clientSide (Thread):
    def __init__(self, player1, player2):
        
        self.port = port
        self.flag = True
        self.host = host
        self.request = sk.socket()
        self.request.connect((self.host, self.port))
        self.sendMessage(firstMessage)
        self.decoded = ""
        self.player1 = player1 # Jugador uno creado en la GUI
        self.player12 = player2 # Jugador dos creado en la GUI
        self.mainTokens = [] #Lista de tokens principales del reto
        self.fillerTokens = [] #Lista de tokens de relleno

        Thread.__init__(self)

        while (self.flag):
            try:
                self.decoded = self.request.recv(bts).decode(format)
                self.processReceived(self.decoded)
            except IOError as e:
                print(e)
        
    def sendMessage(self, message):
        self.message = message
        print("Enviar:", self.message)
        self.out = self.message.encode(format)
        print("Salida antes de enviar:", self.out.decode(format))
        self.sending = self.request.send(self.out)
        print("Se han enviado: {} bytes al servidor.".format(self.sending))
    
    #Método para procesar los mensajes que mande el server

    def processReceived(self, message):
        self.message = message
        try:
            if "Challenges" in self.message:  
                message_dict = json.loads(self.message)          
                with open('JsonResources/CurrentChallenge.json', 'w') as json_file:
                    json.dump(message, json_file) 
                print(json.dumps(message_dict))
                self.readChallenge(self.mainTokens, self.fillerTokens)
                tokenToSend = self.fillerTokens[0]
                self.sendToken(tokenToSend, self.player1.getID())

            elif self.message == "exit":
                self.sendMessage("exit")
                self.flag = False
                self.request.close()
                print("Terminado")
            else:
                print(self.message)    
        except IOError as e:
            print(e)
    
    def getMainTokens(self):
        return self.mainTokens
    def getFillerTokens(self):
        return self.fillerTokens

    def setMainTokens(self, mainTokens):
        self.mainTokens = mainTokens
    def setFillerTokens(self, fillerTokens):
        self.fillerTokens = fillerTokens

    #Método que recibe un token y una id de jugador y que retorna un 
    # mensaje formato json para mandarlo al server
    def sendToken(self, Token, playerID):
        data = {
            "ID" + str(playerID):{
                "Token": {
                    "shape": Token.getShape(),
                    "value": Token.getVal(),
                    "points": Token.getPoints()
                }
            }
        }
        with open('JsonResources/CurrentToken.json', 'w') as write_file:
            json.dump(data, write_file)
        message = json.dumps(data)
        self.sendMessage(message)
        print(message)
        return message
    #Método que toma un diccionario con info de token para parsearlo a objeto de Python
    def jsonToToken(self, tokenDict): 
        return namedtuple('Token', tokenDict.keys())(*tokenDict.values())

    #Esta función se encarga de leer el json donde están los tokens de ese reto
    #estos tokens se agregan a las listas mainTokens y fillerTokens
    def readChallenge(self, mainTokens, fillerTokens):
        file_path = 'JsonResources/CurrentChallenge.json'
        with open(file_path,'r') as read_file:
            data = json.load(read_file)

        data_dict = json.loads(data)
        #mainTokens_dict
        mainTokens_dict = data_dict["Challenges"]["MainTokens"]
        fillerTokens_dict = data_dict["Challenges"]["FillerTokens"]
        #Agregando main tokens
        for key in mainTokens_dict:
            token_dict = mainTokens_dict.get(key)
            token_string = json.dumps(token_dict)
            token_object = json.loads(token_string, object_hook=self.jsonToToken)
            myFinalToken = Token(token_object.value, token_object.shape, token_object.points)
            mainTokens.append(myFinalToken)
        #Agregando filler tokens
        for key in fillerTokens_dict:
            token_dict = fillerTokens_dict.get(key)
            token_string = json.dumps(token_dict)
            token_object = json.loads(token_string, object_hook=self.jsonToToken)
            myFinalToken = Token(token_object.value, token_object.shape, token_object.points)
            fillerTokens.append(myFinalToken) 
        for token in range(len(fillerTokens)):
            print(fillerTokens[token].getPoints())
        
        self.setMainTokens(mainTokens)
        self.setFillerTokens(fillerTokens)
    
    def parsePlayer(self):
        pass

def main():
    player1 = Player(1)
    player2 = Player(2)
      
    c1 = clientSide(player1, player2)
    c1.start()

if __name__ == "__main__":
    main()
print("Client closed....") 
