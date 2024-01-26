import socket
import struct

from Commands import Command
import os

iP = '127.0.0.1'
port = 2121
port_data = 2222
ADDR = (iP, port)
ADDR_data = (iP, port_data)
FORMAT = "utf-8"
SIZE = 1024
PATH = ""
server_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_data.bind(ADDR_data)
def upload():

    print(f"Srever is listening on {ADDR_data}\n")
    connection_data, addr_data = server_data.accept()
    print(f"Client connect on {addr_data}\n")
    msg = "send filename"
    connection_data.sendto(msg.encode(FORMAT), ADDR_data)

    filename = connection_data.recv(SIZE).decode(FORMAT)
    filename = connection_data.recv(SIZE).decode(FORMAT)
    #print(filename+"\n")
    filetype = connection_data.recv(SIZE).decode(FORMAT)
    #print(filetype + "\n")
    file_size = struct.unpack("i", connection_data.recv(SIZE))[0]

    file = open(PATH+filename+filetype, "wb")
    # msg = "send data"
    # connection_data.sendto(msg.encode(FORMAT), ADDR_data)
    s = 0

    while s < file_size:
        data = connection_data.recv(SIZE)
        file.write(data)
        s += SIZE

    msg = "upload file seccesfully finished"
    connection_data.sendto(msg.encode(FORMAT), ADDR_data)

    file.close()
    connection_data.close()

def download():
    print(f"Srever is listening on {ADDR_data}\n")
    connection_data, addr_data = server_data.accept()
    print(f"Client connect on {addr_data}\n")
    msg = "send filepath"
    connection_data.sendto(msg.encode(FORMAT), ADDR_data)

    filepath = connection_data.recv(SIZE).decode(FORMAT)
    print(filepath, end="\n")
    if (not os.path.exists(filepath)):
        msg = "False"
        connection_data.sendto(msg.encode(FORMAT), ADDR_data)
        return
    msg = "True"
    connection_data.sendto(msg.encode(FORMAT), ADDR_data)
    file = open(filepath, "rb")

    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    connection_data.sendto(filename.encode(FORMAT), ADDR_data)
    connection_data.sendto(struct.pack("i", filesize), ADDR_data)
    data = file.read(SIZE)
    while data:
        connection_data.sendto(data, ADDR_data)
        data = file.read(SIZE)
        # connection.sendto(data, ADDR)
    recv = connection_data.recv(SIZE).decode(FORMAT)
    print(recv, end="\n")
    file.close()
    connection_data.close()

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
            server_data.listen(1)
            upload()
        elif (request == Command['DOWNLOAD'].value):
            server_data.listen(1)
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