import socket

iP = '127.0.0.1'
port = 6060
ADDR = (iP, port)
FORMAT = "utf-8"
SIZE = 1024

# def main() :
# if __name__ == '_main_' :

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen(1)
print(f"Srever is listening on {ADDR}\n")
connection, addr = server.accept()
print(f"Client connect on {addr}\n")

while True:
    file_name = connection.recv(SIZE)
    print(f"recive from client(name of data_file) : {file_name.decode(FORMAT)}")
    file = open(f"server_data/{file_name.decode(FORMAT)}_recv", "w")

    msg = "seccesfully recived"
    connection.sendto(msg.encode(FORMAT), ADDR)
    
    data = connection.recv(SIZE)
    print(f"recive from client(data) : {data.decode(FORMAT)}")
    file.write(data.decode(FORMAT))

    msg = "seccesfully recived data"
    connection.sendto(msg.encode(FORMAT), ADDR)

    file.close()


# if __name__ == '_main_' :
#     main()

