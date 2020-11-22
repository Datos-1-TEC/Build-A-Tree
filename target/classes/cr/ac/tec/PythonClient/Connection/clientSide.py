import socket
import json
port = 6666
flag = True
file = 'JsonResources/Player.json'
message = ""

with open(file, 'r') as f:
    player = json.load(f)
    cont = 0

    for item in player['Player']:
        message +=  item + ": " + str(player['Player'][item]) + ","  
message = "{" + "\n 'Player':" + "{" + message[:-1] + "\n}" + "}"  
message = "Hi from client"


while flag:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(('127.0.0.1', port))
    clientSocket.send(test.encode()) 
    flag = False