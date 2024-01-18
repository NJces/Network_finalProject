import socket
from Commands import Command

iP = '127.0.0.1'
port = 2121
ADDR = (iP, port)
FORMAT = "utf-8"
SIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

while True:
    server.listen(1)
    print(f"Srever is listening on {ADDR}\n")
    connection, addr = server.accept()
    print(f"Client connect on {addr}\n")

    request = connection.recv(SIZE).decode(FORMAT)
    if (request == Command['QUIT'].value):
        print("Client disconnected")
        break