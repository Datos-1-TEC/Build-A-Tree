import socket
port = 6666
flag = True
while flag:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(('127.0.0.1', port))
    message = input("type your message and presss enter to send...\n")
    clientSocket.send(message.encode())