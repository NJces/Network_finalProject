import socket
from Commands import Command
import os

iP = '127.0.0.1'
port = 2121
ADDR = (iP, port)
FORMAT = "utf-8"
SIZE = 1024
PATH = "client_download/"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
is_connected = False

def help():
    print("\n===============Helper==============\n")
    print("\"connect\":\t connect to the server\n")
    print("\"upload\":\t upload file to the server\n")
    print("\"download\":\t download file to the server\n")
    print("\"delete\":\t delete file from the server\n")
    print("\"pwd\":\t find current location on server")
    print("\n===============Helper==============\n")
    print("\nyou can enter these command now to communicate with server or ", end="")

def connect(command):
    #client connect to server 
    client.connect(ADDR)
    client.send(command.encode(FORMAT))
    print(f"Client connect to server on {ADDR}\n")

def upload(path, command):
    if (not os.path.exists(path)):
        print("file dosn't exist!")
        return
    
    client.send(command.encode(FORMAT))

    msg = client.recv(SIZE).decode(FORMAT)
    print(msg, end="\n")

    filename = input("please enetr name for uploaded file: ")
    filetype = input("please enetr type for uploaded file: ")
    client.send(filename.encode(FORMAT))
    client.send(filetype.encode(FORMAT))

    msg = client.recv(SIZE).decode(FORMAT)
    print(msg, end="\n")

    file = open(path, "r")
    data = file.read()
    client.send(data.encode(FORMAT))

    msg = client.recv(SIZE).decode(FORMAT)
    print(msg, end="\n")

    file.close()

def download(path, command):
    client.send(command.encode(FORMAT))

    msg = client.recv(SIZE).decode(FORMAT)
    print(msg, end="\n")

    client.send(path.encode(FORMAT))

    msg = client.recv(SIZE).decode(FORMAT)
    print(msg, end="\n")
    if (msg == "False"):#file not found
        print("file not found!")
        return
    filename = client.recv(SIZE).decode(FORMAT)
    data = client.recv(SIZE).decode(FORMAT)
    file = open(PATH+filename, "w")
    file.write(data)
    client.send("file download seccesfully".encode(FORMAT))

    file.close()


def pwd(command):
    client.send(command.encode(FORMAT))

    location = client.recv(SIZE).decode(FORMAT)
    print(f"you are now in \"{location}\" location on Server\n")
    client.send("ok".encode(FORMAT))
    
while True:
    print(f"enter \"{Command['HELP'].value}\" to see command or \"{Command['QUIT'].value}\" if want to exit program\n")
    inp = input()
    if inp == Command['QUIT'].value and is_connected:
        client.send(inp.encode(FORMAT))
        break
    elif inp == Command['HELP'].value:
        help()
    elif inp == Command['CONNECT'].value:
        print(is_connected)
        if (not is_connected):
            connect(inp)
            is_connected = True
        else: print("you have already connected to the server!!")
        recv = client.recv(SIZE).decode(FORMAT)
        print(recv)
    elif inp == Command['UPLOAD'].value and is_connected:
        path = input("please enetr file path you want to upload: ")
        upload(path, inp)
    elif inp == Command['PWD'].value and is_connected:
        pwd(inp)
    elif inp == Command['DOWNLOAD'].value and is_connected:
        path = input("please enetr file path you want to download: ")
        download(path, inp)


client.close()