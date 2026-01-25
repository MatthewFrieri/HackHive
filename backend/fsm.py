from enum import IntEnum
from backend.speech.rstt import STT
from backend.speech.betting import bet
from backend.hw import ESP
from backend.parser import Parser
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

    def init(self, metadata: dict, path='backend/game.json'):
        self.meta = metadata
        self.game_dict = {
            "meta": self.meta,
            "hands": []
        }
        self.write_to_json()

        self.path = path
        self.stt = STT()
        self.stt.run()

        self.esp = ESP()

        self.start_new_hand()

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
        if not Parser.get_curr_stage():
            self.start_new_hand()
        else:
            self.state += 1

    def run(self):

        while True:

            if self.state == State.DEAL_PRE_FLOP:
                self.esp.deal_preflop()
                time.sleep(5)
                self.state = State.BET_PRE_FLOP

                # some sort of state update to get the hole card
                self.write_to_json()

            elif self.state == State.BET_PRE_FLOP:
                self.do_bet()

            elif self.state == State.DEAL_FLOP:
                self.show_steet(3)

            elif self.state == State.BET_FLOP:
                self.do_bet()

            elif self.state == State.DEAL_TURN:
                self.show_steet(1)

            elif self.state == State.BET_TURN:
                self.do_bet()

            elif self.state == State.DEAL_RIVER:
                self.show_street(1)

            elif self.state == State.BET_RIVER:
                self.do_bet()

            # dont think we need this
            elif self.state == State.SHOWDOWN:
                self.state = State.DEAL_PRE_FLOP
