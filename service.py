import argparse
import socket
import threading


def handle_client(conn, addr):
    connected = True
    while connected:
        msg = conn.recv(1024)
        if msg:
            decoded_msg = msg.decode("utf-8")
            if decoded_msg == HEALTH_CHECK_MESSAGE:
                conn.send(HEALTH_CHECK_MESSAGE.encode("utf-8"))
            else:
                print(f"[MESSAGE RECEIVED] from {addr[0]}:{addr[1]}")
                if not decoded_msg.isdigit():
                    conn.send("Invalid message".encode("utf-8"))
                else:
                    number = int(decoded_msg)
                    conn.send(f"It’s instance number {number}".encode("utf-8"))
        else:
            connected = False
    conn.close()


def start():
    server.listen()
    addr = server.getsockname()
    print(f"[LISTENING] Server is listening on {addr[0]}:{addr[1]}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


parser = argparse.ArgumentParser()
parser.add_argument("-p", type=int, default=0)
args = parser.parse_args()

PORT = args.p
SERVER = "localhost"
HEALTH_CHECK_MESSAGE = "!HEALTH_CHECK"
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

start()
