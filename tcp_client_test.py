import socket

iP = '127.0.0.1'
port = 6060
ADDR = (iP, port)
FORMAT = "utf-8"
SIZE = 1024

def upload(path):
    file = open(path, "r")
    data = file.read()
    return data
    file.close()

# def main() :
# if __name__ == '_main_' :
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print(f"Client connect to server on {ADDR}\n")
# file = open("client_data/test1.txt", "r")
client.send("test1".encode(FORMAT))

msg = client.recv(SIZE)
print(f"recive from server : {msg.decode(FORMAT)}\n")

data = upload("client_data/test1.txt")
client.send(data.encode(FORMAT))

msg = client.recv(SIZE)
print(f"recive from server : {msg.decode(FORMAT)}\n")


# if __name__ == '_main_' :
#     main()
