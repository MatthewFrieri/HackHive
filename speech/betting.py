from backend.parser import Parser
import json

def bet(path, stt):

    while Parser.get_stage().endswith('bets'):

        old_state = stt.get_state()
        stt.start_listening()

        new_state = old_state
        while new_state == old_state:
            new_state = stt.get_state()

        stt.stop_listening()

        with open(path, "r") as f:
            game = json.load(f)
        
        stage = Parser.get_stage().split("_")[0]
        if stage not in game['hands'][-1].keys():
            game['hands'][-1][stage] = {}
        game['hands'][-1][stage] = new_state[1]
