import sys
import socket as sk
import json
host = "127.0.0.1"
port = 6666
flag = True
format = "utf8"
file = 'JsonResources/Player.json'
bts = 4096
data = {
    "Player": {
        "ID": 2,
        "miNodo": 45,
        "posicion": "x, y"
    }
}

with open('JsonResources/Player2.json', 'w') as write_file:
    json.dump(data, write_file)
message = json.dumps(data)

class client:
    def __init__(self, port, host):

        self.port = port
        self.flag = True
        self.host = host
        self.request = sk.socket()
        self.request.connect((self.host, self.port))
        
        print("Conectado")

    def hostListener(self, message):
        self.flag = True
        self.message = message
        count = 0
        while self.flag:
            if count == 0:
                toServer = self.message
                print("Enviar:", toServer)
                out = toServer.encode(format)
                print("Salida antes de enviar:", out.decode(format))
                sending = self.request.send(out)
                print("Se han enviado: {} bytes al servidor.".format(sending))
                fromServer = self.request.recv(bts)
                decoded = fromServer.decode(format)
                print("Servidor retorna:", decoded)
                count += 1

            else:
                toServer = input("Texto para enviar: ")
                print("Enviar:", toServer)
                out = toServer.encode(format)
                print("Salida antes de enviar:", out.decode(format))
                sending = self.request.send(out)
                print("Se han enviado: {} bytes al servidor.".format(sending))
                if toServer == "exit":
                    self.flag = False
                    break
                fromServer = self.request.recv(bts)
                decoded = fromServer.decode(format)
                print("Servidor retorna:", decoded)
        if self.flag == False:
            self.request.close()
            print("Terminado")

c1 = client(port, host)
c1.hostListener(message)

""" def main():

    c1 = client(port, host)
    c1.hostListener(message)

if __name__ == "__main__":
    main()
print("Client closed....")
  """   
