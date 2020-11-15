import socket
port = 6666
flag = True
while flag:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(('localhost', port))
    message = input("type your message and presss enter to send...\n")
    clientSocket.send(message.encode())