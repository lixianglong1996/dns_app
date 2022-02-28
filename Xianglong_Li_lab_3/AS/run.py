import socket
import os
import json
from socket import *


def check_database():
    if os.path.exists("database.json"):
        pass
    else:
        with open("database.json", 'w') as f:
            init_data = {}
            f.write(json.dumps(init_data, ensure_ascii=False, indent=4))

    database = {}
    with open("database.json", 'r') as f:
        database = json.loads(f.read())
    return database


def write_database(database):
    with open("database.json", 'w') as f:
        f.write(json.dumps(database, ensure_ascii=False, indent=4))


def server_loop():
    database = check_database()
    server = socket(AF_INET, SOCK_DGRAM)
    server.bind(('', 53533))
    while True:
        print("AS: Start Listening...")
        message, addr = server.recvfrom(2048)
        message = json.loads(message.decode())
        print("Message:{}".format(message))
        if len(message) == 4:
            print("deal Registration")
            # (Name, Value, Type, TTL)
            hostname = message.get('Name')
            database[hostname] = message
            write_database(database)
            server.sendto('201'.encode(), addr)
        elif len(message) == 2:
            print("DNS Query")
            # (Name, Type)
            hostname = message.get('Name')
            server.sendto(json.dumps(database.get(hostname)).encode(), addr)

if __name__ == "__main__":
    server_loop()
