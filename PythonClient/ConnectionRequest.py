from json.decoder import JSONDecoder
from socket import *
import threading


class ConnectionRequest:
    def __init__(self):
        
        self.port = 6666
        self.flag = True
        self.request = socket(AF_INET,SOCK_STREAM)
        self.request.connect(('localhost', self.port))
        threading.Thread.__init__(self)
        while(self.flag):
            message = self.request.recv(4096)
            processMessage(message)
            
    def processMessage(message):
        if message.find("%"):
            print(message)
        else:
            print("processing message... "+ message)

    def sendMessage(message):
        self.request.send(message.encode())
        print("Message sent")


connectionRequest = ConnectionRequest()
connectionRequest.sendMessage("Hi from client")





    
            


