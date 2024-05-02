import socket
import threading
import argparse


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg = conn.recv(1024)
        if msg:
            if msg.decode("utf-8") == DISCONNECT_MESSAGE:
                connected = False
            elif msg.decode("utf-8") == HEALTH_CHECK_MESSAGE:
                conn.send("OK".encode("utf-8"))
            else:
                print(f"[MESSAGE RECEIVED] from {addr[0]}:{addr[1]}")
                number = int(msg.decode("utf-8"))
                conn.send(f"It’s instance number {number}".encode("utf-8"))
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
parser.add_argument("-p", type=int, default=0)
args = parser.parse_args()

PORT = args.p
SERVER = "localhost"
DISCONNECT_MESSAGE = "!DISCONNECT"
HEALTH_CHECK_MESSAGE = "!HEALTH_CHECK"
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

start()
