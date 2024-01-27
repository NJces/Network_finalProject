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
def showList():
    #os.getcwd() +
    list_files = os.listdir("./server_data")
    connection.send(struct.pack("i", len(list_files)))
    for i in list_files:
        connection.send(struct.pack("i", sys.getsizeof(i)))
        connection.send(i.encode('utf-8'))
        connection.send(struct.pack("i", os.stat("./server_data/" + i).st_size))
        connection.recv(SIZE)
    print("Successfully sent file listing")
    return
def delete():
    fname_length = struct.unpack("h", connection.recv(2))[0]
    fname = connection.recv(fname_length)
    if os.path.isfile(fname):
        os.remove(fname)

def cd():
    global PATH
    dir_name = connection.recv(SIZE).decode(FORMAT)
    print(dir_name)
    # if (dir_name == ".." and PATH != "server_data/"):
    #     head, tail = os.path.split(PATH)
    #     print(head, end="\n")
    #     print(tail)
    #     PATH = head
    #     msg = "True"
    #     connection.sendto(msg.encode(FORMAT), ADDR)
    #     return
    if (not existDir(dir_name)): 
        msg = "False"
        connection.sendto(msg.encode(FORMAT), ADDR)
        return
    msg = "True"
    connection.sendto(msg.encode(FORMAT), ADDR)
    PATH = os.path.join(PATH, dir_name+"/")

def existDir(dir_name):
    global PATH
    parent_directory = PATH.rstrip('/')
    subdirectories = [d for d in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, d))]
    if dir_name in subdirectories:
        print(f"The directory '{parent_directory}' contains the directory '{dir_name}'.")
        return True
    else:
        print(f"The directory '{parent_directory}' does not contain the directory '{dir_name}'.")
        return False

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
        elif (request == Command['LIST'].value):
            showList()
        elif (request == Command['DELETE'].value):
            delete()
        elif (request == Command['CD'].value):
            cd()
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