from enum import IntEnum
from speech.rstt import STT
from speech.betting import bet
from hw import ESP
from parser import Parser
import time
import json

class State(IntEnum):

    DEAL_PRE_FLOP = 0
    BET_PRE_FLOP = 1
    DEAL_FLOP = 2
    BET_FLOP = 3
    DEAL_TURN = 4
    BET_TURN = 5
    DEAL_RIVER = 6
    BET_RIVER = 7
    SHOWDOWN = 8


class HandFSM:

    def __init__(self, metadata: dict, path='game.json'):
        self.meta = metadata
        self.game_dict = {
            "meta": self.meta,
            "hands": []
        }

        self.path = path
        self.stt = STT()
        self.stt.start()

        self.esp = ESP(len(self.meta['players']))

        self.start_new_hand()
        self.write_to_json()

    def read_from_json(self):
        with open(self.path, "r") as f:
            self.game_dict = json.load(f)

    def write_to_json(self):
        with open(self.path, "w") as f:
            json.dump(self.game_dict, f)

    def start_new_hand(self): 
        self.state = State.DEAL_PRE_FLOP

    def show_street(self, num_cards):
        self.esp.deal_n(num_cards)
        time.sleep(5)
        self.state += 1

        # state update for flop
        self.write_to_json()

    def do_bet(self):
        bet(self.path, self.stt)
        self.read_from_json()
        if Parser.get_curr_stage(self.game_dict) == 'showdown':
            self.start_new_hand()
        else:
            self.state += 1

    def run(self):

        while True:

            if self.state == State.DEAL_PRE_FLOP:
                sb_pos = Parser.get_position_data(self.game_dict)["small_blind_pos"]
                self.esp.deal_preflop(sb_pos)
                time.sleep(5)
                self.state = State.BET_PRE_FLOP

                # some sort of state update to get the hole card
                self.write_to_json()

            elif self.state == State.BET_PRE_FLOP:
                print("PRE FLOB BETTING")
                self.do_bet()
                print("PRE FLOP BETTING DONE")

            elif self.state == State.DEAL_FLOP:
                print("DEALING FLOP")
                self.show_street(3)

            elif self.state == State.BET_FLOP:
                print("FLOP BETTING")
                self.do_bet()

            elif self.state == State.DEAL_TURN:
                print("DEALING TURN")
                self.show_street(1)

            elif self.state == State.BET_TURN:
                print("TURN BETTING")
                self.do_bet()

            elif self.state == State.DEAL_RIVER:
                self.show_street(1)

            elif self.state == State.BET_RIVER:
                self.do_bet()

            # dont think we need this
            elif self.state == State.SHOWDOWN:
                self.state = State.DEAL_PRE_FLOP

if __name__ == '__main__':
    F = HandFSM({
        "status": "ongoing",

        "players": {
        "0": "mat",
        "1": "dav",
        "2": "adr"
        },
        "big_blind": 10,
        "small_blind": 5,
        "buy_in": 200
    })
    F.run()
