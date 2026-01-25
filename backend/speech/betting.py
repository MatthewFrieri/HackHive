from backend.parser import Parser
import time
import json

def bet(path, stt):
    with open(path, "r") as f:
        game = json.load(f)
    while Parser.get_curr_stage(game).endswith('bets'):

        old_state = stt.get_state()
        new_state = old_state
        while new_state == old_state:
            time.sleep(0.5)
            new_state = stt.get_state()

        with open(path, "r") as f:
            game = json.load(f)
        
        stage = Parser.get_curr_stage(game)
        print(stage)


        # if stage.startswith("pre_flop"):
        #     game['hands'].append({})

        if stage not in game['hands'][-1].keys():
            game['hands'][-1][stage] = []
        game['hands'][-1][stage].append(new_state[1])


        with open(path, "w") as f:
            json.dump(game, f)

        time.sleep(0.5)
    print("DONE BETTING")
