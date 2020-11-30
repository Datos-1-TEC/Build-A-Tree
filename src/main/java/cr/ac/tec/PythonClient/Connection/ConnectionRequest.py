import sys
import socket as sk
import json
host = "127.0.0.1"
port = 6666
bts = 4096
format = "utf8"
flag = True
file = 'JsonResources/Player.json'
data = {
    "Player" :{
        "ID": 2,
        "miNodo": 45,
        "posicion": "x, y"
}
}

with open('JsonResources/Player2.json', 'w') as write_file:
    json.dump(data, write_file)       

message = json.dumps(data)

socketClient =  sk.socket()
socketClient.connect((host, port))
print("Conectado")

count = 0
while True: 
    if count == 0:
        toServer = message
        print("Enviar:", toServer)
        out = toServer.encode(format)
        print("Salida antes de enviar:", out.decode(format))
        sending = socketClient.send(out)
        print("Se han enviado: {} bytes al servidor.".format(sending))   
        fromServer = socketClient.recv(bts)
        decoded = fromServer.decode(format)
        print("Servidor retorna:", decoded)
        count += 1

    else:
        toServer = input("Texto para enviar: ")
        print("Enviar:", toServer)
        out = toServer.encode(format)
        print("Salida antes de enviar:", out.decode(format))
        sending = socketClient.send(out)
        print("Se han enviado: {} bytes al servidor.".format(sending))   
        if toServer == "exit":
            break
        fromServer = socketClient.recv(bts)
        decoded = fromServer.decode(format)
        print("Servidor retorna:", decoded)
        
socketClient.close()
print("Terminado")





    
            


