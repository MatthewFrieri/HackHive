from enum import Enum
from treys import Card, Evaluator

from equity_calculator.table import HoldemTable

class Action(Enum):
    FOLD = "F"
    CHECK = "X"
    CALL = "C"
    RAISE = "R"

class PosIterator:
    # Starts iterating on the small blind

    def __init__(self, items: list, dealer_index: int):
        self.items = list(items) # Make a copy
        self.start_index = (dealer_index + 1) % len(items)
        self.index = self.start_index

    def next(self) -> str:
        value = self.items[self.index]
        self.index = (self.index + 1) % len(self.items)
        return value
 
    def peek(self) -> str:
        return self.items[self.index]
    
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
    def _handle_actions(it: PosIterator, actions: list, pos_bets: dict, pos_stacks: dict, pos_last_actions: dict):
        last_raise_pos = None
        start_pos = it.peek()

        if len(actions) == 0:
            raise Exception("There must be at least one action")
        
        for action in actions:
            pos = it.next()

            if action == Action.FOLD.value:
                it.remove(pos)
            elif action == Action.CHECK.value:
                pass
            elif action == Action.CALL.value:
                diff = max(pos_bets.values()) - pos_bets[pos]
                pos_bets[pos] += diff
                pos_stacks[pos] -= diff
            elif action.startswith(Action.RAISE.value):
                diff = max(pos_bets.values()) - pos_bets[pos]
                raise_amount = int(action[1:])
                pos_bets[pos] += diff + raise_amount
                pos_stacks[pos] -= diff + raise_amount
                last_raise_pos = pos
            else:
                raise Exception("Invalid betting action")
            
            pos_last_actions[pos] = action

        is_over_by_fold = len(it.remaining()) == 1

        # Full circle of checks and folds (or checks, folds, and calls on pre flop)
        if last_raise_pos is None and start_pos == it.peek():
            return True, is_over_by_fold
        
        # There was a raise and everyone else called or folded
        if last_raise_pos == it.peek() and not actions[-1].startswith(Action.RAISE.value):
            return True, is_over_by_fold
        
        return False, is_over_by_fold
    
    @staticmethod
    def _get_winner(pre_flop: dict, board: list):
        board = [Card.new(card) for card in board]
        evaluator = Evaluator()
        pos_eval = {}
        for pos in pre_flop:
            hand = [Card.new(card) for card in pre_flop[pos]]
            pos_eval[pos] = evaluator.evaluate(board, hand)
        return min(pos_eval, key=pos_eval.get) # Lower eval is better

    @classmethod
    def _handle_hand_end(cls, it: PosIterator, hand: dict, pos_bets: dict, pos_stacks: dict):
        if len(it.remaining()) == 1:
            winner = it.next()
        else:
            positions = it.remaining()
            pre_flop = {k: v for k, v in hand["pre_flop"].items() if k in positions}
            board = hand["flop"] + [hand["turn"]] + [hand["river"]]
            winner = cls._get_winner(pre_flop, board)
        pot = sum(pos_bets.values())
        for pos in pos_bets.keys():
            if pos == winner:
                pos_stacks[pos] += pot
        for pos in pos_bets:
            pos_bets[pos] = 0

    @classmethod
    def get_position_data(cls, game: dict):
        position_names = game["meta"]["players"]
        res = {"players": position_names}

        curr_hand_index = len(game["hands"]) - 1
        res["small_blind_pos"] = (curr_hand_index + 1) % len(position_names)
        res["big_blind_pos"] = (curr_hand_index + 2) % len(position_names)

        return res
    
    @classmethod
    def get_card_data(cls, game):
        if len(game['hands']) == 0:
            curr_hand = {}
            game['hands'].append(curr_hand)
        else:
            curr_hand = game["hands"][-1]

        board = []
        if "flop" in curr_hand:
            board += curr_hand["flop"]
        if "turn" in curr_hand:
            board.append(curr_hand["turn"])
        if "river" in curr_hand:
            board.append(curr_hand["river"])

        return {"holes": curr_hand["pre_flop"], "board": board}

    @classmethod
    def get_state(cls, game: dict):
        positions = game["meta"]["players"].keys()
        pos_stacks = {pos: game["meta"]["buy_in"] for pos in positions}
        pos_last_actions = {pos: "" for pos in positions}
        sb = game["meta"]["small_blind"]
        bb = game["meta"]["big_blind"]

        for hand_index, hand in enumerate(game["hands"]):

            dealer_index = hand_index % len(positions)
            pos_bets = {pos: 0 for pos in positions}

            it = PosIterator(positions, dealer_index)
            for blind in [sb, bb]:
                pos = it.next()
                pos_bets[pos] += blind
                pos_stacks[pos] -= blind

            if "pre_flop_bets" not in hand: break
            is_betting_over, is_over_by_fold = cls._handle_actions(it, hand["pre_flop_bets"], pos_bets, pos_stacks, pos_last_actions)

            if is_betting_over and not is_over_by_fold:
                it.reset()
                if "flop_bets" not in hand: break
                is_betting_over, is_over_by_fold = cls._handle_actions(it, hand["flop_bets"], pos_bets, pos_stacks, pos_last_actions)
            
            if is_betting_over and not is_over_by_fold:
                it.reset()
                if "turn_bets" not in hand: break
                is_betting_over, is_over_by_fold = cls._handle_actions(it, hand["turn_bets"], pos_bets, pos_stacks, pos_last_actions)

            if is_betting_over and not is_over_by_fold:
                it.reset()
                if "river_bets" not in hand: break
                is_betting_over, is_over_by_fold = cls._handle_actions(it, hand["river_bets"], pos_bets, pos_stacks, pos_last_actions)
            
            if is_betting_over:
                cls._handle_hand_end(it, hand, pos_bets, pos_stacks)

        curr_player = it.peek()
        pot = sum(pos_bets.values())
        return {
            "curr_player": curr_player, 
            "pot": pot, 
            "bets": pos_bets, 
            "stacks": pos_stacks, 
            "last_actions": pos_last_actions
        }
    
    @classmethod
    def get_equity_data(cls, game: dict):
        positions = game["meta"]["players"].keys()
        card_data = cls.get_card_data(game)
        table = HoldemTable(num_players=len(positions), deck_type="full")

        for position in positions:
            player_num = int(position) + 1
            table.add_to_hand(player_num, card_data["holes"][position])
        
        table.add_to_community(card_data["board"])
        equities = table.simulate(odds_type="win_any")
        
        for k in list(equities.keys()):
            if "Player" in k:
                player_num = int(k.split(" ")[-1])
                equities[str(player_num - 1)] = equities[k]
                del equities[k]
        return equities
    
    @classmethod
    def get_meta_data(cls, game: dict):
        return {k:v for k,v in game["meta"].items() if k in ["small_blind", "big_blind", "buy_in"]}

    @classmethod
    def get_curr_stage(cls, game: dict):
        positions = game["meta"]["players"].keys()
        pos_bets = {pos: 0 for pos in positions}
        pos_stacks = {pos: game["meta"]["buy_in"] for pos in positions}
        pos_last_actions = {pos: "" for pos in positions}
        sb = game["meta"]["small_blind"]
        bb = game["meta"]["big_blind"]

        if len(game['hands']) == 0:
            hand = {}
            game['hands'].append(hand)
        else:
            hand = game["hands"][-1]

        it = PosIterator(positions, 0)
        for blind in [sb, bb]:
            pos = it.next()
            pos_bets[pos] += blind
            pos_stacks[pos] -= blind

        if "pre_flop_bets" not in hand: return ""
        is_betting_over, is_over_by_fold = cls._handle_actions(it, hand["pre_flop_bets"], pos_bets, pos_stacks, pos_last_actions)
        if not is_betting_over: return "pre_flop_bets"
        
        if not is_over_by_fold:
            it.reset()
            if "flop_bets" not in hand: return ""
            is_betting_over, is_over_by_fold = cls._handle_actions(it, hand["flop_bets"], pos_bets, pos_stacks, pos_last_actions)
            if not is_betting_over: return "flop_bets"

        if not is_over_by_fold:
            it.reset()
            if "turn_bets" not in hand: return ""
            is_betting_over, is_over_by_fold = cls._handle_actions(it, hand["turn_bets"], pos_bets, pos_stacks, pos_last_actions)
            if not is_betting_over: return "turn_bets"

        if not is_over_by_fold:
            it.reset()
            if "river_bets" not in hand: return ""
            is_betting_over, is_over_by_fold = cls._handle_actions(it, hand["river_bets"], pos_bets, pos_stacks, pos_last_actions)
            if not is_betting_over: return "river_bets"

        return ""

    @classmethod
    def get_everything(cls, game: dict):
        return {
            "positions": cls.get_position_data(game),
            "cards": cls.get_card_data(game),
            "state": cls.get_state(game),
            "equities": cls.get_equity_data(game),
            "meta": cls.get_meta_data(game),
        }
