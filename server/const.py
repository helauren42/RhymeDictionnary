import socket

def getPort():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    addr = s.getsockname()
    return addr[1]

HOST="127.0.0.1"
PORT=getPort()

PROJECT_DIR = "/home/henri/Projects/RhymeDictionnary/"
