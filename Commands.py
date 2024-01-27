from enum import Enum

class Command(Enum):
    QUIT = "quit"
    HELP = "help"
    CONNECT = "connect"
    UPLOAD = "upload"
    DOWNLOAD = "download"
    PWD = "pwd"
    DELETE = "delete"
    LIST = "list"
    CD = "cd"
    def Iscommand(input):
        isCmd = False
        for cmd in Command:
            if input == cmd.value:
                isCmd = True
        return isCmd