from socket import *

def connect_to_remote(host, port):
    with socket(AF_INET, SOCK_STREAM) as connection:
        connection.connect((host, port))
        return connection

def connect_to_local(location):
    with socket(AF_UNIX, SOCK_STREAM) as connection:
        connection.connect(location)
        return connection 