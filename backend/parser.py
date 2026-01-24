from enum import Enum
from treys import Card, Evaluator

class Action(Enum):
    FOLD = "F"
    CHECK = "X"
    CALL = "C"
    RAISE = "R"

class Status(Enum):
    ONGOING = "ongoing"
    ENDED = "ended"

class PositionIterator:
    # Starts iterating on the small blind

    def __init__(self, items: list, dealer_index: int):
        self.items = list(items) # Make a copy
        self.start_index = (dealer_index + 1) % len(items)
        self.index = self.start_index

    def __iter__(self):
        return self

    def __next__(self):
        if not self.items:
            raise StopIteration
        value = self.items[self.index]
        self.index = (self.index + 1) % len(self.items)
        return value

    def remaining(self) -> list:
        return self.items

    def reset(self):
        self.index = self.start_index

    def remove(self, value) -> bool:
        if value not in self.items:
            raise KeyError
        idx = self.items.index(value)
        self.items.pop(idx)

        if idx < self.index:
            self.index -= 1
        if idx < self.start_index:
            self.start_index -= 1
        if self.index >= len(self.items):
            self.index = 0
        if self.start_index >= len(self.items):
            self.start_indexindex = 0

        if len(self.items) == 0:
            raise Exception("Can not remove last player")

class Parser:

    @staticmethod
    def handle_action(it: PositionIterator, action: str, position_bets: dict):
        pos = next(it)

        if action == Action.FOLD.value:
            it.remove(pos)
            return len(it.remaining()) == 1
        elif action == Action.CHECK.value:
            pass
        elif action == Action.CALL.value:
            position_bets[pos] = max(position_bets.values())
        elif action.startswith(Action.RAISE.value):
            raise_amount = int(action[1:])
            position_bets[pos] = max(position_bets.values()) + raise_amount
        else:
            raise Exception("Invalid betting action")
        return False
    
    @staticmethod
    def get_winner(pre_flop: dict, board: list):
        board = [Card.new(card) for card in board]
        evaluator = Evaluator()
        pos_eval = {}
        for pos in pre_flop:
            hand = [Card.new(card) for card in pre_flop[pos]]
            pos_eval[pos] = evaluator.evaluate(board, hand)
        return min(pos_eval, key=pos_eval.get) # Lower eval is better

    @classmethod
    def handle_hand_over(cls, it: PositionIterator, hand: dict, position_bets: dict, position_stacks: dict):
        if len(it.remaining()) == 1:
            winner = next(it)
        else:
            positions = it.remaining()
            pre_flop = {k: v for k, v in hand["pre_flop"].items() if k in positions}
            board = hand["flop"] + [hand["turn"]] + [hand["river"]]
            winner = cls.get_winner(pre_flop, board)
        pot = sum(position_bets.values())
        for pos in position_bets.keys():
            if pos == winner:
                position_stacks[pos] += pot - position_bets[winner]
            else:
                position_stacks[pos] -= position_bets[pos]

    @classmethod
    def get_stacks(cls, game: dict):
        positions = list(game["meta"]["players"].keys())
        position_stacks = {pos: game["meta"]["buy_in"] for pos in positions}
        sb = game["meta"]["small_blind"]
        bb = game["meta"]["big_blind"]

        for hand_index, hand in enumerate(game["hands"]):
            if hand["status"] != Status.ENDED.value:
                raise Exception("Can not compute stacks when all hands are not ended")

            dealer_index = hand_index % len(positions)
            is_hand_over = False
            position_bets = {pos: 0 for pos in positions}

            it = PositionIterator(positions, dealer_index)
            position_bets[next(it)] = sb # Skip SB
            position_bets[next(it)] = bb # Skip BB
            for action in hand["pre_flop_bets"]:
                is_hand_over |= cls.handle_action(it, action, position_bets)

            if not is_hand_over:
                it.reset()
                for action in hand["flop_bets"]:
                    is_hand_over |= cls.handle_action(it, action, position_bets)

            if not is_hand_over:
                it.reset()
                for action in hand["turn_bets"]:
                    is_hand_over |= cls.handle_action(it, action, position_bets)

            if not is_hand_over:
                it.reset()
                for action in hand["river_bets"]:
                    cls.handle_action(it, action, position_bets)
            
            cls.handle_hand_over(it, hand, position_bets, position_stacks)

        return position_stacks


import json

with open("example_game.json", "r") as f:
    game = json.load(f)

    print(Parser.get_stacks(game))
