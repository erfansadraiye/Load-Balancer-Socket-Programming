import argparse
import threading
import socket
import time


class Client:
    def __init__(self, server, port, number):
        self.number = number
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((server, port))

    def send(self, msg):
        message = msg.encode("utf-8")
        self.client.send(message)
        print(f"Client {self.number} send message: {msg}")
        received = self.client.recv(1024).decode("utf-8")
        if received:
            print(f"Client {self.number} received message: {msg}")

    def disconnect(self):
        # self.send("!DISCONNECT")
        self.client.close()
        print(f"Client {self.number} disconnected")


parser = argparse.ArgumentParser()
parser.add_argument("--request_per_second", type=int, default=3)
parser.add_argument("--total_time", type=int, default=3)
parser.add_argument("--client_count", type=int, default=5)
parser.add_argument("--balancerPort", type=int, default=8080)
parser.add_argument("--balancerIp", type=str, default='localhost')
args = parser.parse_args()

PORT = args.balancerPort
SERVER = "localhost"
ADDR = (SERVER, PORT)
REQUESTS_PER_SECOND = args.request_per_second
TOTAL_TIME = args.total_time
CLIENT_COUNT = args.client_count


def start_client(client_number):
    client = Client(SERVER, PORT, client_number)
    print(f"Client {client_number} connected to {SERVER}:{PORT}")
    for k in range(TOTAL_TIME):
        for j in range(REQUESTS_PER_SECOND):
            client.send(str(client_number * 100 + k * REQUESTS_PER_SECOND + j + 1))
        time.sleep(1)
    client.disconnect()


threads = []
for i in range(CLIENT_COUNT):
    thread = threading.Thread(target=start_client, args=(i+1,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("All clients disconnected")
