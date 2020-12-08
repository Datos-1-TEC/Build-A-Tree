import sys
import socket as sk
import json
from threading import*
host = "127.0.0.1"
port = 6666
flag = True
format = "utf8"
bts = 4096

firstMessage = "Connected"

class clientSide (Thread):
    def __init__(self):
        
        self.port = port
        self.flag = True
        self.host = host
        self.request = sk.socket()
        self.request.connect((self.host, self.port))
        self.sendMessage(firstMessage)
        self.decoded = ""
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

    def processReceived(self, message):
        self.message = message
        
        if self.message == "Temporizador iniciado":
            print(self.message)

        elif self.message == "challenges":
            print(self.message)

        elif self.message == "exit":
            self.sendMessage("exit")
            self.flag = False
            self.request.close()
            print("Terminado")
        else:
            print(self.message)
        
        
def main():
    c1 = clientSide()
    c1.start()

if __name__ == "__main__":
    main()
print("Client closed....")

        




