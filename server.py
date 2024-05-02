import argparse
import json
import socket
import time
import threading
from itertools import cycle


class Server:

    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (host, port)

    def check_connection(self):
        return True
        # try:
        #     self.server.send(HEALTH_CHECK_MESSAGE.encode("utf-8"))
        #     resp = self.server.recv(1024)
        #     if resp.decode("utf-8") == "OK":
        #         return True
        #     return False
        # except:
        #     return False

    def disconnect(self):
        self.server.send(DISCONNECT_MESSAGE.encode("utf-8"))
        self.server.close()

    def try_to_connect(self):
        try:
            self.server.connect(self.addr)
            return True
        except:
            return False

    """
    Send a message to the server and get the response
    """

    def send(self, msg):
        self.server.send(msg)
        received = self.server.recv(1024)
        if received:
            return received
        return None


servers = []
iter_servers = cycle(servers)


def schedule_refresh():
    global REFRESH_RATE
    while True:
        time.sleep(REFRESH_RATE)
        refresh_servers()


def refresh_servers():
    global iter_servers
    available_servers = []
    for s in servers:
        if s.check_connection():
            available_servers.append(s)
        else:
            print(f"Failed to connect to {s.addr[0]}:{s.addr[1]}")
    print(f"[SERVERS] {len(available_servers)} servers available")
    iter_servers = cycle(available_servers)


# def initialize_servers():
#     global iter_servers, servers
#     with open("config.json") as f:
#         data = json.load(f)
#         for server in data["servers"]:
#             s = Server(server["host"], server["port"])
#             if s.try_to_connect():
#                 servers.append(s)
#             else:
#                 print(f"Failed to connect to {server['host']}:{server['port']}")
#     print(f"Connected to {len(servers)} servers")
#     iter_servers = cycle(servers)


def initialize_servers():
    global iter_servers, servers
    with open("config.txt") as f:
        text = f.read()
        servers_text = text.split("\n")
        for server_text in servers_text:
            if server_text == "":
                continue
            server = server_text.split()
            s = Server(server[0], int(server[1]))
            if s.try_to_connect():
                servers.append(s)
            else:
                print(f"Failed to connect to {server[0]}:{server[1]}")
    print(f"Connected to {len(servers)} servers")
    iter_servers = cycle(servers)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg = conn.recv(1024)
        if msg:
            if msg.decode("utf-8") == DISCONNECT_MESSAGE:
                connected = False
            elif msg.decode("utf-8").isnumeric():
                next_server = next(iter_servers)
                print(
                    f"[MESSAGE RECEIVED] from {addr[0]}:{addr[1]} and forwarded to {next_server.addr[0]}:{next_server.addr[1]}")
                response = next_server.send(msg)
                if response:
                    conn.send(response)
                else:
                    conn.send("Server not available".encode("utf-8"))
            else:
                "Invalid message received"


    print(f"[CONNECTION CLOSED] {addr} disconnected.")
    conn.close()


def start():
    server.listen()
    addr = server.getsockname()
    print(f"[LISTENING] Server is listening on {addr[0]}:{addr[1]}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


parser = argparse.ArgumentParser()
parser.add_argument("-p", type=int, default=8080)
parser.add_argument("-refreshRate", type=int, default=60)
args = parser.parse_args()

PORT = args.p
REFRESH_RATE = args.refreshRate
SERVER = "localhost"
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
HEALTH_CHECK_MESSAGE = "!HEALTH_CHECK"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

initialize_servers()

# t = threading.Thread(target=schedule_refresh)
# t.start()

start()
