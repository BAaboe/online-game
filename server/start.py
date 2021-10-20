

from request_handler import RequestHandler
import threading
import argparse
import os


quit = False


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--player", required=False)
    args = parser.parse_args()

    return args


def start():

    args = parse_args()
    if args.player:
        with open("num_of_players", "w") as f:
            f.write(args.player)
    else:
        with open("num_of_players", "w") as f:
            f.write("4")

    hand = None
    while True:
        nw = RequestHandler()

        thread = threading.Thread(target=nw.connection_thread, daemon=True)
        thread.start()

        if not hand:
            hand = threading.Thread(target=get_input)
            hand.start()
        else:
            if not thread.is_alive():
                hand = threading.Thread(target=get_input)
                hand.start()

        thread.join()
        print("Game Finished")


def get_input():
    while True:
        try:
            inp = input()
            if inp == "exit":
                os._exit(0)
        except Exception as e:
            print("cant fuck with me, looser")


if __name__ == "__main__":
    start()
