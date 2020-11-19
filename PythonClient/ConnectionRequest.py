import socket
import struct
import threading
import Queue
import time


class ConnectionRequest(threading.Thread):
    def __init__(self):
        
        self.port = 6666
        self.flag = True
        self.request = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("socket created")
        self.request.connect(('localhost', self.port))
        threading.Thread.__init__(self)
        while(self.flag):
            message = self.request.recv(4096)
            processMessage(message)
        threading.Thread.start()  

    def processMessage(self, message):
        if message.find("%"):
            print(message)
        else:
            print("processing message... "+ message)

    def sendMessage(self,message):
        self.request.send(message.encode())
        print("Message sent")


connectionRequest = ConnectionRequest()
connectionRequest.sendMessage("Hi from client")





    
            


