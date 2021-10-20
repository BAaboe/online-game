import request_handler


class Game(object):
    PLAYERS = 0

    def __init__(self, players):
        """
        :param players: Player
        """
        self.players = players
        self.round = 0
        self.sentences = []

        with open("num_of_players", "r") as f:
            self.PLAYERS = int(f.readline())

    def scramble_sentence(self, sentence):
        words = sentence.split(' ')
        final = []
        for word in words:
            chars = []
            for char in word:
                chars.append(char)

            count = 0
            for index in range(len(chars)):
                print()
                if (index + 1) % 4 == 0 or index == 0:
                    count += 1
                    pass
                else:
                    chars[index] = '*'

            final.append(''.join(chars))

        return " ".join(final)

    def append_sentence(self, sentence):
        self.sentences.append(sentence)

    def get_first_sentence(self):
        request_handler.broadcast(self.players, {"status": 5})
        request_handler.broadcast(self.players[:self.round] + self.players[self.round + 1:], {"status": 0})
        data = self.players[0].send({"status": 1})
        self.append_sentence(data["msg"])
        self.round += 1

    def send_get_sentence(self):
        request_handler.broadcast(self.players[:self.round] + self.players[self.round + 1:], {"status": 0})
        msg = self.sentences[-1]

        scrambled_msg = self.scramble_sentence(msg)

        data = self.players[self.round].send({"status": 2, "msg": scrambled_msg})
        self.append_sentence(data["msg"])
        self.round += 1

    def main(self):
        self.get_first_sentence()
        for i in range(self.PLAYERS - 1):
            self.send_get_sentence()
        request_handler.broadcast(self.players, {"status": 3, "msg": self.sentences})
        request_handler.broadcast(self.players, {"status": 4})
