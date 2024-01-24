import socket
from Commands import Command
import os

iP = '127.0.0.1'
port = 2121
ADDR = (iP, port)
FORMAT = "utf-8"
SIZE = 1024
PATH = ""

def upload():
    msg = "send filename"
    connection.sendto(msg.encode(FORMAT), ADDR)

    filename = connection.recv(SIZE).decode(FORMAT)
    filetype = connection.recv(SIZE).decode(FORMAT)
    file = open(PATH+filename+filetype, "w")

    msg = "send data"
    connection.sendto(msg.encode(FORMAT), ADDR)

    data = connection.recv(SIZE).decode(FORMAT)
    file.write(data)

    msg = "upload file seccesfully finished"
    connection.sendto(msg.encode(FORMAT), ADDR)

    file.close()

def download():
    msg = "send filepath"
    connection.sendto(msg.encode(FORMAT), ADDR)

    filepath = connection.recv(SIZE).decode(FORMAT)
    print(filepath, end="\n")
    if (not os.path.exists(filepath)):
        msg = "False"
        connection.sendto(msg.encode(FORMAT), ADDR)
        return
    msg = "True"
    connection.sendto(msg.encode(FORMAT), ADDR)
    file = open(filepath, "r")

    filename = os.path.basename(filepath)
    data = file.read()
    connection.sendto(filename.encode(FORMAT), ADDR)
    connection.sendto(data.encode(FORMAT), ADDR)

    recv = connection.recv(SIZE).decode(FORMAT)
    print(recv, end="\n")

def response():
    while True:
        request = connection.recv(SIZE).decode(FORMAT)
        if (request == Command['QUIT'].value):
            print("Client disconnected")
            break
        elif (request == Command['CONNECT'].value):
            msg = f"you are now in \"{PATH}\""
            connection.sendto(msg.encode(FORMAT), ADDR)
        elif (request == Command['UPLOAD'].value):
            upload()
        elif (request == Command['DOWNLOAD'].value):
            download()
        elif (request == Command['PWD'].value):
            connection.sendto(PATH.encode(FORMAT), ADDR)
            ackMsg = connection.recv(SIZE).decode(FORMAT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

while True:
    server.listen(1)
    print(f"Srever is listening on {ADDR}\n")
    connection, addr = server.accept()
    print(f"Client connect on {addr}\n")
    PATH = "server_data/"

    response()