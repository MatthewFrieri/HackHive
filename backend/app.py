from flask import Flask, jsonify, request
from flask_cors import CORS
import json

from parser import Parser
from fsm import HandFSM

app = Flask(__name__)
CORS(app)

@app.route("/data", methods=["GET"])
def data():
    f = open("example_game.json", "r")
    game = json.load(f)
    return jsonify(Parser.get_everything(game))

@app.route("/start_game", methods=["POST"])
def start_game():
    data = request.get_json()

    game_dict = {
        "meta": {
            "players": {str(i): p for i, p in enumerate(data.get("players", []))},
            "small_blind": data.get("smallBlind"),
            "big_blind": data.get("bigBlind"),
            "buy_in": data.get("buyIn"),
        },
        "hands": []
    }

    fsm = HandFSM(game_dict)
    fsm.run()

    return jsonify({"status": "ok"})
