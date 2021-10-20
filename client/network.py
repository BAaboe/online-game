import socket
import json


class Network(object):
    def __init__(self, ip, port, name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.addr = (self.ip, self.port)
        self.name = name

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.client.sendall(self.name.encode())
            return json.loads(self.client.recv(2048).decode())
        except Exception as e:
            self.disconnect(e)

    def send(self, data):
        try:
            self.client.send(json.dumps(data).encode())

        except socket.error as e:
            self.disconnect(e)

    def disconnect(self, msg):
        print("Disconnected from server:", msg)
        self.client.close()

    def catch_broadcast(self, last):
        data = None
        try:
            data = self.client.recv(2048).decode()
        except ConnectionError as e:
            if last == 7:
                print("\nConnection Error: Server is gone!")
            else:
                print("Connection Error: Server is gone!")
            quit()
        data = json.loads(data)

        return data

