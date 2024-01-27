import socket
import struct
import sys

from Commands import Command
import os

iP = '127.0.0.1'
port = 2121
port_data = 2222
ADDR = (iP, port)
ADDR_data = (iP, port_data)
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

def connect_data(path):
    #client connect to server
    client_data.connect(ADDR_data)
    client_data.send(path.encode(FORMAT))
    print(f"Client connect to server on {ADDR_data}\n")
def showList(command):
    client.send(command.encode(FORMAT))
    number_of_files = struct.unpack("i", client.recv(4))[0]
    for i in range(int(number_of_files)):
        fname_size = struct.unpack("i", client.recv(4))[0]
        fname = client.recv(fname_size)
        fsize = struct.unpack("i", client.recv(4))[0]
        print("\t{} - {}b".format(fname, fsize))
        client.send("1".encode('utf-8'))

def upload(path, command):
    connect_data(path)
    if (not os.path.exists(path)):
        print("file dosn't exist!")
        return
    msg = client_data.recv(SIZE).decode(FORMAT)
    print(msg, end="\n")

    filename = input("please enetr name for uploaded file: ")
    filetype = input("please enetr type for uploaded file: ")
    #client_data.send(filename.encode(FORMAT))
    client_data.sendto(filename.encode(FORMAT), ADDR_data)
    #client_data.send(filetype.encode(FORMAT))
    client_data.sendto(filetype.encode(FORMAT), ADDR_data)
    # msg = client_data.recv(SIZE).decode(FORMAT)
    # print(msg, end="\n")
    file = open(path, "rb")
    # filename = os.path.basename(path)
    filesize = os.path.getsize(path)
    client_data.sendto(struct.pack("i", filesize), ADDR_data)
    data = file.read(SIZE)
    while data:
        client_data.sendto(data, ADDR_data)
        data = file.read(SIZE)

    # msg = client_data.recv(SIZE).decode(FORMAT)
    # print(msg, end="\n")

    file.close()
    client_data.close()

def download(path, command):
    connect_data(path)
    msg = client_data.recv(SIZE).decode(FORMAT)
    print(msg, end="\n")

    client_data.send(path.encode(FORMAT))

    msg = client_data.recv(SIZE).decode(FORMAT)
    print(msg, end="\n")
    if (msg == "False"):#file not found
        print("file not found!")
        return
    filename = client_data.recv(SIZE).decode(FORMAT)
    file_size = struct.unpack("i", client_data.recv(SIZE))[0]
    #data = client_data.recv(SIZE).decode(FORMAT)
    file = open(PATH+filename, "wb")
    s = 0
    while s < file_size:
        data = client_data.recv(SIZE)
        file.write(data)
        s += SIZE
    client_data.send("file download seccesfully".encode(FORMAT))

    file.close()
    client_data.close()
def delete(command):
    client.send(command.encode(FORMAT))
    fname = input("please enetr file path you want to delete: ")
    client.send(struct.pack("h", sys.getsizeof(fname)))
    client.send(fname.encode(FORMAT))
def pwd(command):
    client.send(command.encode(FORMAT))

    location = client.recv(SIZE).decode(FORMAT)
    print(f"you are now in \"{location}\" location on Server\n")
    client.send("ok".encode(FORMAT))

def cd(command):
    client.send(command.encode(FORMAT))

    # msg = client.recv(SIZE).decode(FORMAT)
    # print(msg, end="\n")

    dir_name = input("please enter name of directory or \"..\" to back : ")
    client.send(dir_name.encode(FORMAT))

    msg = client.recv(SIZE).decode(FORMAT)
    if (msg == "False"):
        print("directory not found!!")
        return
    pwd("pwd")

    
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
        client_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.send(inp.encode(FORMAT))
        upload(path, inp)
    elif inp == Command['PWD'].value and is_connected:
        pwd(inp)
    elif inp == Command['DOWNLOAD'].value and is_connected:
        client_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.send(inp.encode(FORMAT))
        path = input("please enetr file path you want to download: ")
        download(path, inp)
    elif inp == Command['LIST'].value and is_connected:
        showList(inp)
    elif inp == Command['DELETE'].value and is_connected:
        delete(inp)
    elif inp == Command['CD'].value and is_connected:
        cd(inp)

client.close()