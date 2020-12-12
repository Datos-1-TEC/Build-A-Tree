import sys
import socket as sk
import json
from threading import*
from json import JSONEncoder
from PlayerSocket import*
from TokenSocket import*
from collections import namedtuple
host = "127.0.0.1"
port = 6666
flag = True
format = "utf8"
bts = 4096

firstMessage = "Connected"
class clientSide (Thread):
    def __init__(self, player1_socket, player2_socket):
        
        self.port = port
        self.flag = True
        self.host = host
        self.request = sk.socket()
        self.request.connect((self.host, self.port))
        self.sendMessage(firstMessage)
        self.decoded = ""
        self.player1_socket = player1_socket # Jugador uno creado en la GUI
        self.player2_socket = player2_socket # Jugador dos creado en la GUI
        self.mainTokens = [] #Lista de tokens principales del reto
        self.fillerTokens = [] #Lista de tokens de relleno
        self.onGame = False
        self.level = 0
        self.depth  = 0
        self.order = 0
        self.numElements = 0

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
#-------------------------------------------------------------------------------------#    
    #Método para procesar los mensajes que mande el server
    def processReceived(self, message):
        self.message = message
        try:
            if "Challenges" in self.message:  
                message_dict = json.loads(self.message)          
                with open('JsonResources/CurrentChallenge.json', 'w') as json_file:
                    json.dump(message, json_file) 
                print(json.dumps(message_dict))
                self.mainTokens = []
                self.fillerTokens = []
                self.readChallenge(self.mainTokens, self.fillerTokens)
                tokenToSend = self.mainTokens[0]
                self.sendToken(tokenToSend, self.player1_socket.getID())

            elif self.message == "exit":
                self.sendMessage("exit")
                self.flag = False
                self.request.close()
                print("Terminado")
            
            elif self.message == "True":
                self.setOnGame(True)
                print("Iniciar temporizador")
                print("\n")

            elif "player1" in self.message:
                self.updatePlayerScore(self.player1_socket, self.message)
                print("El puntaje actual es: ")
                print(self.player1_socket.getScore())

            elif "player2" in self.message:
                self.updatePlayerScore(self.player2_socket, self.message)
                print("El puntaje actual es: ")
                print(self.player2_socket.getScore())
                print("\n")

            elif "depth" in self.message:
                splitted_message = self.message.split(":") 
                newDepth = int(splitted_message[1])
                self.setDepth(newDepth)
                print("La profundidad es: " + str(self.getDepth))
                print("\n")
            elif "Order" in self.message and "Level" in self.message:
                splitted_message = self.message.split(":")
                order = int(splitted_message[1])
                level = int(splitted_message[3])
                self.setOrder(order)
                self.setLevel(level)  
                print("El orden del BTree es: " + str(self.getOrder()))
                print("El nivel del BTree es: " + str(self.getLevel()))
                print("\n")

            elif "numElements" in self.message:
                splitted_message = self.message.split(":") 
                newNumElements = int(splitted_message[1])
                self.setNumElements(newNumElements)
                print("La cantidad de elementos del arbol es: " + str(self.getNumElements()))
                print("\n")

            else:
                print(self.message)    
        except IOError as e:
            print(e)
#----------------------------------Bloque de getters----------------------------------#
    def getOnGame(self):
        return self.getOnGame
    def getMainTokens(self):
        return self.mainTokens
    def getFillerTokens(self):
        return self.fillerTokens   
    def getLevel(self):
        return self.level
    def getOrder(self):
        return self.order
    def getDepth(self):
        return self.depth   
    def getNumElements(self):
        return self.numElements
#----------------------------------Bloque de setters----------------------------------#
    def setMainTokens(self, mainTokens):
        self.mainTokens = mainTokens
    def setFillerTokens(self, fillerTokens):
        self.fillerTokens = fillerTokens
    def setOnGame(self, boolean):
        self.onGame = boolean      
    def setLevel(self, level):
        self.level = level
    def setOrder(self, order):
        self.order = order
    def setDepth(self, depth):
        self.depth = depth
    def setNumElements(self, numElements):
        self.numElements = numElements

#--------------------------Actualizar el puntaje del jugador--------------------------#
    def updatePlayerScore(self, player, message):
        splitted_Info =  message.split(":")
        print("La info del puntaje es")
        print(splitted_Info)
        currentScore = int(splitted_Info[1])
        player.setScore(currentScore)
#-------------------------------------------------------------------------------------#
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
#-------------------------------------------------------------------------------------#    
    #Método que toma un diccionario con info de token para parsearlo a objeto de Python
    def jsonToToken(self, tokenDict): 
        return namedtuple('Token', tokenDict.keys())(*tokenDict.values())
#-------------------------------------------------------------------------------------#
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
            myFinalToken = TokenSocket(token_object.value, token_object.shape, token_object.points)
            mainTokens.append(myFinalToken)
        #Agregando filler tokens
        for key in fillerTokens_dict:
            token_dict = fillerTokens_dict.get(key)
            token_string = json.dumps(token_dict)
            token_object = json.loads(token_string, object_hook=self.jsonToToken)
            myFinalToken = TokenSocket(token_object.value, token_object.shape, token_object.points)
            fillerTokens.append(myFinalToken) 
        for token in range(len(fillerTokens)):
            print(fillerTokens[token].getPoints())
        
        self.setMainTokens(mainTokens)
        self.setFillerTokens(fillerTokens)
#-------------------------------------------------------------------------------------#    
    def parsePlayer(self):
        pass

def main():
    player1_socket = PlayerSocket(1)
    player2_socket = PlayerSocket(2)
      
    c1 = clientSide(player1_socket, player2_socket)
    c1.start()

if __name__ == "__main__":
    main()
print("Client closed....") 
