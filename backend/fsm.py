from enum import IntEnum
from backend.speech.rstt import STT
from backend.speech.betting import bet
from backend.hw import ESP
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

    def run(self):

        while True:

            if self.state == State.DEAL_PRE_FLOP:
                self.esp.deal_preflop()
                time.sleep(5)
                self.state = State.BET_PRE_FLOP

                # some sort of state update to get the hole card
                self.write_to_json()

            elif self.state == State.BET_PRE_FLOP:
                bet(self.path, self.stt)
                self.read_from_json()
                self.state = State.DEAL_FLOP

            elif self.state == State.DEAL_FLOP:
                self.esp.deal_flop()
                time.sleep(5)
                self.state = State.BET_PRE_FLOP

                # state update for flop
                self.write_to_json()

            elif self.state == State.BET_FLOP:
                bet(self.path, self.stt)
                self.read_from_json()
                self.state = State.DEAL_TURN

            elif self.state == State.DEAL_TURN:
                self.esp.deal_one()
                time.sleep(3)
                self.state = State.BET_TURN

                # state update for turn
                self.write_to_json()

            elif self.state == State.BET_TURN:
                bet(self.path, self.stt)
                self.read_from_json()
                self.state = State.DEAL_RIVER

            elif self.state == State.DEAL_RIVER:
                self.esp.deal_one()
                time.sleep(3)
                self.state = State.BET_RIVER

                # state update for river
                self.write_to_json()

            elif self.state == State.BET_RIVER:
                bet(self.path, self.stt)
                self.read_from_json()
                self.state = State.SHOWDOWN

            # dont think we need this
            elif self.state == State.SHOWDOWN:
                self.state = State.DEAL_PRE_FLOP