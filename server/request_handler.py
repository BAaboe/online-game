import socket
import json
from Player import Player
from Game import Game


def broadcast(players, data):
    for player in players:
        player.conn.send(json.dumps(data).encode())
        ret = player.conn.recv(2048).decode()
        if int(ret) == 0:
            pass


def send(conn, data):
    conn.send(json.dumps(data).encode())
    try:
        data = conn.recv(2048)
        data = json.loads(data.decode())
        return data
    except socket.error as e:
        str(e)


def just_send(conn, data):
    conn.send(json.dumps(data).encode())
    ret = conn.recv(2048).decode()
    if int(ret) == 0:
        pass


class RequestHandler(object):
    PLAYERS = 0
    game_running = True

    def __init__(self):
        self.connection_queen = []
        self.game = None
        with open("num_of_players", "r") as f:
            self.PLAYERS = int(f.readline())

    def handle_queen(self, player):
        self.connection_queen.append(player)

        if len(self.connection_queen) >= self.PLAYERS:
            print("Game Started")
            broadcast(self.connection_queen, {"status": 71, "msg": player.name})
            broadcast(self.connection_queen, {"status": 7, "msg": f"{len(self.connection_queen)}/{self.PLAYERS}"})
            return True, self.connection_queen
        else:
            player.just_send({"status": 6})
            broadcast(self.connection_queen, {"status": 71, "msg": player.name})
            broadcast(self.connection_queen, {"status": 7, "msg": f"{len(self.connection_queen)}/{self.PLAYERS}"})
            return False

    def authentication(self, conn, addr):
        try:
            data = conn.recv(1024)
            name = str(data.decode())
            if not name:
                raise Exception("No name received")

            conn.send("1".encode())

            player = Player(addr, name, conn)
        except socket.error as e:
            print(e)
        print(f"{name} connected")

        return self.handle_queen(player)

    def connection_thread(self):
        server = ""
        port = 5556

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((server, port))
        except socket.error as e:
            str(e)

        s.listen(1)
        print("Waiting for a connection, Game Started")

        while self.game_running:
            conn, addr = s.accept()
            print("New connection!")

            full = self.authentication(conn, addr)
            try:
                if full[0]:
                    game = Game(full[1])
                    game.main()
                    break
            except TypeError as e:
                pass

        s.close()

