import request_handler


class Player(object):
    def __init__(self, ip, name, conn):
        self.ip = ip
        self.name = name
        self.conn = conn
        self.guessed = False

    def send(self, data):
        back = request_handler.send(self.conn, data)
        return back

    def just_send(self, data):
        request_handler.just_send(self.conn, data)
