import argparse
import socket
import threading
import time
from itertools import cycle


class Server:

    def __init__(self, host, port):
        self.addr = (host, port)

    def check_connection(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(self.addr)
            s.send(HEALTH_CHECK_MESSAGE.encode("utf-8"))
            received = s.recv(1024)
            if received:
                if received.decode("utf-8") == HEALTH_CHECK_MESSAGE:
                    s.close()
                    return True
            s.close()
            return False
        except:
            return False

    def send(self, msg):
        """
        Send a message to the server and get the response
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(self.addr)
            s.send(msg)
            received = s.recv(1024)
            if received:
                s.close()
                return received
            s.close()
            print(f"Failed to get response from {self.addr[0]}:{self.addr[1]}")
            return None
        except:
            print(f"Failed to get response from {self.addr[0]}:{self.addr[1]}")
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
            if s.check_connection():
                servers.append(s)
            else:
                print(f"Failed to connect to {server[0]}:{server[1]}")
    print(f"Connected to {len(servers)} servers")
    iter_servers = cycle(servers)


def handle_client(conn, addr):
    connected = True
    while connected:
        msg = conn.recv(1024)
        if msg:
            next_server = next(iter_servers)
            print(f"[MESSAGE RECEIVED] from {addr[0]}:{addr[1]}"
                  f" and forwarded to {next_server.addr[0]}:{next_server.addr[1]}")
            response = next_server.send(msg)
            if response:
                conn.send(response)
            else:
                conn.send("Server not available".encode("utf-8"))
        else:
            connected = False
    conn.close()


def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    addr = server.getsockname()
    print(f"[LISTENING] Server is listening on {addr[0]}:{addr[1]}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


parser = argparse.ArgumentParser()
parser.add_argument("-p", type=int, default=8080)
parser.add_argument("-refreshRate", type=int, default=60)
args = parser.parse_args()

PORT = args.p
REFRESH_RATE = args.refreshRate
SERVER = "localhost"
ADDR = (SERVER, PORT)
HEALTH_CHECK_MESSAGE = "!HEALTH_CHECK"

initialize_servers()

t = threading.Thread(target=schedule_refresh)
t.start()

start()
