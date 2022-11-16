from socket import *


def connect_to_remote(host, port):
    connection = socket(AF_INET, SOCK_STREAM)
    connection.connect((host, port))
    return connection


def connect_to_local(location):
    connection = socket(AF_UNIX, SOCK_STREAM)
    connection.connect(location)
    return connection
