import socket
import json
port = 6666
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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    try:
        clientSocket.connect(('localhost', port))
    except Exception as e:
        raise SystemExit(f"No pudo conectarse al server, pues : {e}")
    while flag:
        firstMsg = input("Message to server is: ")
        if firstMsg == "Send Json":
            clientSocket.send(message.encode('utf-8'))
        else:

            clientSocket.send(firstMsg.encode('utf-8'))
            break
        
        received  = clientSocket.recv(1024)
        print(f"Server message: {received.decode('utf-8')}")
        