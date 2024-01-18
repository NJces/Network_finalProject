import socket
from Commands import Command

iP = '127.0.0.1'
port = 2121
ADDR = (iP, port)
FORMAT = "utf-8"
SIZE = 1024
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

def connect():
    #client connect to server 
    client.connect(ADDR)
    print(f"Client connect to server on {ADDR}\n")

while True:
    print(f"enter \"{Command['HELP'].value}\" to see command or \"{Command['QUIT'].value}\" if want to exit program\n")
    inp = input()
    if (Command.Iscommand(inp) and is_connected):
        print("YSE")
        client.send(inp.encode(FORMAT))
    if inp == Command['QUIT'].value:
        break
    if inp == Command['HELP'].value:
        help()
    if inp == Command['CONNECT'].value:
        print(is_connected)
        if (not is_connected):
            connect()
            is_connected = True
        else: print("you have already connected to the server!!")


client.close()