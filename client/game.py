from network import Network
import sys
import os

def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError as e:
        print(e)
        import sys, termios    #for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

class Game(object):
    def __init__(self):
        self.ip = input("Enter ip: ")
        self.port = 5556
        self.username = input("Enter a username: ")
        self.network = Network(self.ip, self.port, self.username)
        self.round = 0

    def parse_status(self):
        last_status = None
        guessed = False
        while True:
            catched_broadcast = self.network.catch_broadcast(last_status)
            parsed_status = catched_broadcast["status"]
            if "msg" in catched_broadcast:
                msg = catched_broadcast["msg"]

            if parsed_status == 0:
                if last_status != 0:
                    if guessed:
                        print("Waiting for the other players to finish")
                    else:
                        print("Waiting for your turn")
                #TODO: make it so it only send it once

            elif parsed_status == 1:
                print("Enter a Sentence: ")
                flush_input()
                sentence = input("")
                status = self.network.send({"status": 1, "msg": sentence})
                guessed = True

            elif parsed_status == 2:
                print(msg)
                print("What do you think this sentence is?")
                flush_input()
                send_msg = input("")
                send_status = {"status": 1, "msg": send_msg}
                self.network.send(send_status)
                guessed = True

            elif parsed_status == 3:
                sentences = msg

                first_sentence = sentences[0]
                final_sentence = sentences[-1]

                print(f"\nThe original sentence was: {first_sentence}"
                      f" and the final guess is {final_sentence}", end="\n\n")
            elif parsed_status == 4:
                self.network.disconnect("Game finished")
                break
            elif parsed_status == 5:

                if last_status == 7:
                    print("\nGame started.")
                else:
                    print("Game started")
            elif parsed_status == 6:
                print("Waiting for players ")

            elif parsed_status == 7:
                print(msg, end="", flush=True)

            elif parsed_status == 71:
                print("\r" + msg + " joined the Game!")

            else:
                print("Unknown status code.")

            last_status = parsed_status
            self.network.client.send("0".encode())

    def main(self):
        status = self.network.connect()
        self.parse_status()


if __name__ == "__main__":
    while True:
        if sys.platform.startswith("win"):
            os.system("cls")
        else:
            os.system("clear")
        game = Game()
        game.main()

        print("\nWant to play again(y/n)?")
        flush_input()
        inp = input("")
        if inp.lower() == "n":
            break
